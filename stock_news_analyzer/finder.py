import logging
import re
from datetime import date as date_obj
from datetime import datetime

import requests
from bs4 import BeautifulSoup, Tag  # Tag를 명시적으로 import
from requests.exceptions import RequestException

from stock_news_analyzer.utils.company_code import COMPANY_CODE

logger = logging.getLogger(__name__)


def get_news_link(
    code: str | None = None,
    company: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    max_pages: int = 10  # 최대 페이지 수 제한
) -> list[dict[str, str]] | None:
    """뉴스 링크를 가져옵니다.

    Args:
        code (str | None, optional): 관련 뉴스를 가져올 코드.
        company (str | None, optional): 관련 뉴스를 가져올 회사 이름.
        date_from (str | None, optional): 시작 날짜 (YYYY.MM.DD 형식).
        date_to (str | None, optional): 종료 날짜 (YYYY.MM.DD 형식).

    Returns:
        list[dict[str, str]] | None: 뉴스 링크 목록 또는 None.
            - 성공 시: 각 뉴스 항목에 대한 딕셔너리 목록 반환.
              각 딕셔너리는 'date' (날짜), 'title' (제목), 'link' (링크) 키를 포함.
            - 실패 시: None 반환.
    """
    if code is None:
        if company is None:
            logger.warning("code 또는 company가 필요합니다.")
            return None
        if company not in COMPANY_CODE:
            logger.warning("잘못된 company가 주어졌습니다.")
            return None

    _code: str = (
        code if code is not None
        else COMPANY_CODE.get(company or '', '')
    )  # company가 없을 경우 빈 문자열 반환

    crawled_links: list[dict[str, str]] = []
    page: int = 1
    today = date_obj.today()

    while page <= max_pages:
        print(f"페이지 {page}를 가져오고 있습니다.")  # 진행 상황 출력
        try:
            url = f"https://finance.naver.com/item/news_news.nhn?code={_code}&page={page}"
            response = requests.get(url, timeout=10)  # 10초 타임아웃 설정
            response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
            source_code = response.text
        except RequestException as e:
            logger.error(f"요청 실패: {e}")
            break

        html = BeautifulSoup(source_code, "lxml")

        news_items = html.select("table.type5 tr")
        print(f"페이지 {page}에서 {len(news_items)}개의 뉴스를 찾았습니다.")

        if not news_items:
            break  # 더 이상 뉴스가 없으면 루프 종료

        stop_crawling = False
        for item in news_items:
            date_elem = item.select_one(".date")
            if not date_elem:
                continue

            date = date_elem.get_text().strip()
            info_elem = item.select_one(".info")
            source = info_elem.get_text().strip() if info_elem else ""

            title_elem = item.select_one(".title")
            if title_elem and isinstance(title_elem, Tag):
                title_text = title_elem.get_text(strip=True)
                title_text = re.sub("\n", "", title_text) if title_text else ""
                link_elem = title_elem.find('a')
                if link_elem and isinstance(link_elem, Tag):
                    link = f"https://finance.naver.com{link_elem.get('href', '')}"
                else:
                    continue
            else:
                continue

            try:
                news_date = datetime.strptime(date, "%Y.%m.%d %H:%M")
            except ValueError:
                print(f"잘못된 날짜 형식: {date}")
                continue

            # 현재 날짜보다 미래의 뉴스는 무시
            if news_date.date() > today:
                print(f"미래의 뉴스 건너뛰기: {date}")
                continue

            if date_from:
                start_date = datetime.strptime(date_from, "%Y.%m.%d").date()
                if news_date.date() < start_date:
                    print(f"시작 날짜 이전의 뉴스를 발견했습니다: {date}. 크롤링을 중단합니다.")
                    stop_crawling = True
                    break

            if date_to:
                end_date = datetime.strptime(date_to, "%Y.%m.%d").date()
                if news_date.date() > end_date:
                    print(f"종료 날짜 이후의 뉴스 건너뛰기: {date}")
                    continue

            crawled_links.append({
                "date": date,
                "source": source,
                "title": title_text,
                "link": link
            })
            print(f"Added news: {date} - {title_text}")

        if stop_crawling:
            break

        page += 1

    return crawled_links if crawled_links else None
