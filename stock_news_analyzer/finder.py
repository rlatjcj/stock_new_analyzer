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
    """Get news links.

    Args:
        code (str | None, optional): Code to get related news.
        company (str | None, optional): Company name to get related news.
        date_from (str | None, optional): Start date in YYYY.MM.DD format.
        date_to (str | None, optional): End date in YYYY.MM.DD format.
    """
    if code is None:
        if company is None:
            logger.warning("code or company is required.")
            return None
        if company not in COMPANY_CODE:
            logger.warning("wrong company name is given.")
            return None

    _code: str = (
        code if code is not None
        else COMPANY_CODE.get(company or '', '')
    )  # company가 없을 경우 빈 문자열 반환

    crawled_links: list[dict[str, str]] = []
    page: int = 1
    today = date_obj.today()

    while page <= max_pages:
        print(f"Fetching page {page}...")  # 진행 상황 출력
        try:
            url = f"https://finance.naver.com/item/news_news.nhn?code={_code}&page={page}"
            response = requests.get(url, timeout=10)  # 10초 타임아웃 설정
            response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
            source_code = response.text
        except RequestException as e:
            logger.error(f"Request failed: {e}")
            break

        html = BeautifulSoup(source_code, "lxml")

        news_items = html.select("table.type5 tr")
        print(f"Found {len(news_items)} news items on page {page}")

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
                print(f"Invalid date format: {date}")
                continue

            # 현재 날짜보다 미래의 뉴스는 무시
            if news_date.date() > today:
                print(f"Skipping future news: {date}")
                continue

            if date_from:
                start_date = datetime.strptime(date_from, "%Y.%m.%d").date()
                if news_date.date() < start_date:
                    print(f"Found news before start date: {date}. Stopping crawling.")
                    stop_crawling = True
                    break

            if date_to:
                end_date = datetime.strptime(date_to, "%Y.%m.%d").date()
                if news_date.date() > end_date:
                    print(f"Skipping news after end date: {date}")
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
