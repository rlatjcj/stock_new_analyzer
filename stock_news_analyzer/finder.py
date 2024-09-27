from datetime import datetime
from typing import Any, Dict, List, Optional

import aiohttp
from bs4 import BeautifulSoup, Tag

from stock_news_analyzer.utils.company_code import COMPANY_CODE
from stock_news_analyzer.utils.logger import get_logger

logger = get_logger(__name__)


def clean_title(title: str) -> str:
    return title.strip()


async def fetch(session: aiohttp.ClientSession, url: str) -> Any:
    async with session.get(url) as response:
        return await response.text()


async def get_news_link(
    code: Optional[str] = None,
    company: Optional[str] = None,
    date_from: str = "",
    date_to: str = "",
    max_pages: int = 1,
) -> List[Dict[str, Any]]:
    """뉴스 링크를 비동기적으로 가져옵니다.

    Args:
        code (str | None, optional): 관련 뉴스를 가져올 코드.
        company (str | None, optional): 관련 뉴스를 가져올 회사 이름.
        date_from (str | None, optional): 시작 날짜 (YYYY.MM.DD 형식).
        date_to (str | None, optional): 종료 날짜 (YYYY.MM.DD 형식).
        max_pages (int, optional): 크롤링할 최대 페이지 수.
    Returns:
        list[dict[str, str]] | None: 뉴스 링크 목록 또는 None.
            - 성공 시: 각 뉴스 항목에 대한 딕셔너리 목록 반환.
              각 딕셔너리는 'date' (날짜), 'title' (제목), 'link' (링크) 키를 포함.
            - 실패 시: None 반환.
    """
    if code is None:
        if company is None:
            logger.warning("code 또는 company가 필요합니다.")
            return []
        if company not in COMPANY_CODE:
            logger.warning("잘못된 company가 주어졌습니다.")
            return []

    _code: str = (
        code if code is not None
        else COMPANY_CODE.get(company or '', '')
    )

    crawled_links: List[Dict[str, Any]] = []
    today = datetime.now().date()

    async with aiohttp.ClientSession() as session:
        for page in range(1, max_pages + 1):
            url = f"https://finance.naver.com/item/news_news.nhn?code={_code}&page={page}"
            html_content = await fetch(session, url)
            html = BeautifulSoup(html_content, "lxml")

            # relation_lst 클래스를 가진 tr과 그 하위 요소들을 모두 제외
            for relation_lst in html.select("tr.relation_lst"):
                relation_lst.decompose()

            # 남은 tr 요소들 중 hide_news 클래스를 가진 것을 제외하고 선택
            news_items = html.select("table.type5 tbody tr:not(.hide_news)")

            for item in news_items:
                logger.debug(item.text)

            for item in news_items:
                date_elem = item.select_one(".date")
                if not date_elem:
                    logger.debug("날짜 요소를 찾지 못했습니다.")
                    continue

                date = date_elem.get_text().strip()
                info_elem = item.select_one(".info")
                source = info_elem.get_text().strip() if info_elem else ""

                title_elem = item.select_one(".title")
                if title_elem and isinstance(title_elem, Tag):
                    title_text = title_elem.get_text(strip=True)
                    title_text = clean_title(title_text)
                    link_elem = title_elem.find('a')
                    if link_elem and isinstance(link_elem, Tag):
                        link = f"https://finance.naver.com{link_elem.get('href', '')}"
                    else:
                        logger.debug("링크 요소를 찾지 못했습니다.")
                        continue
                else:
                    logger.debug("제목 요소를 찾지 못했습니다.")
                    continue

                try:
                    news_date = datetime.strptime(date, "%Y.%m.%d %H:%M")
                except ValueError:
                    logger.debug(f"잘못된 날짜 형식: {date}")
                    continue

                if news_date.date() > today:
                    logger.debug(f"미래의 뉴스 건너뛰기: {date}")
                    continue

                if date_from:
                    start_date = datetime.strptime(date_from, "%Y.%m.%d").date()
                    if news_date.date() < start_date:
                        logger.debug(
                            f"시작 날짜 이전의 뉴스를 발견했습니다: {date}. 크롤링을 중단합니다.")
                        break

                if date_to:
                    end_date = datetime.strptime(date_to, "%Y.%m.%d").date()
                    if news_date.date() > end_date:
                        logger.debug(f"종료 날짜 이후의 뉴스 건너뛰기: {date}")
                        continue

                crawled_links.append({
                    "date": date,
                    "source": source,
                    "title": title_text,
                    "link": link
                })
                logger.debug(f"Added news: {date} - {title_text}")

    logger.info(f"총 {len(crawled_links)}개의 뉴스를 찾았습니다.")
    return crawled_links


def inspect_date_format(date_str: str) -> bool:
    date_format = "%Y.%m.%d"
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        logger.error(f"잘못된 날짜 형식입니다: {date_str}. YYYY.MM.DD 형식으로 입력해주세요.")
        return False


async def get_news_list(
    company: str,
    date_from: str,
    date_to: str,
    max_pages: int
) -> List[Dict[str, Any]]:
    # 날짜 형식 검증
    if not all(inspect_date_format(date) for date in [date_from, date_to]):
        return []

    logger.info(f"뉴스 검색 시작: 회사 - {company}, 기간 - {date_from} ~ {date_to}")

    # 해당 날짜의 뉴스 가져오기
    news_links: List[Dict[str, Any]] = await get_news_link(
        code=company if company.isdigit() else None,
        company=company if not company.isdigit() else None,
        date_from=date_from,
        date_to=date_to,
        max_pages=max_pages
    )

    logger.info(f"총 {len(news_links)}개의 뉴스를 찾았습니다.")

    if news_links:
        logger.info(f"총 {len(news_links)}개의 뉴스 링크를 찾았습니다:")
        for news in news_links:
            logger.info(f"[{news['date']}] {news['title']} - {news['link']}")
    else:
        logger.info("뉴스 링크가 없습니다.")

    return news_links
