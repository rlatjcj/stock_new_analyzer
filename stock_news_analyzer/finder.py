import asyncio
import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import aiohttp
from bs4 import BeautifulSoup, Tag  # Tag를 명시적으로 import  # Tag를 명시적으로 import

from stock_news_analyzer.utils.company_code import COMPANY_CODE

logger = logging.getLogger(__name__)


def clean_title(title: str) -> str:
    return re.sub(r'\[.*?\]|\(.*?\)|…|\.\.\.', '', title).strip()


async def fetch(session: aiohttp.ClientSession, url: str) -> Any:
    async with session.get(url) as response:
        return await response.text()


async def get_news_link(
    code: Optional[str] = None,
    company: Optional[str] = None,
    date_from: str = "",
    date_to: str = "",
    max_pages: int = 100,
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
    )  # company가 없을 경우 빈 문자열 반환

    crawled_links: List[Dict[str, Any]] = []
    unique_titles = set()
    unique_links = set()
    today = datetime.now().date()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(1, max_pages + 1):
            url = f"https://finance.naver.com/item/news_news.nhn?code={_code}&page={page}"
            tasks.append(fetch(session, url))

        pages = await asyncio.gather(*tasks)

        for page_num, source_code in enumerate(pages, start=1):
            html = BeautifulSoup(source_code, "lxml")
            news_items = html.select("table.type5 tr")
            logger.info(f"페이지 {page_num}에서 {len(news_items)}개의 뉴스를 찾았습니다.")

            if not news_items:
                break

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
                        stop_crawling = True
                        break

                if date_to:
                    end_date = datetime.strptime(date_to, "%Y.%m.%d").date()
                    if news_date.date() > end_date:
                        logger.debug(f"종료 날짜 이후의 뉴스 건너뛰기: {date}")
                        continue

                clean_title_text = clean_title(title_text)

                if clean_title_text in unique_titles or link in unique_links:
                    logger.debug(f"중복된 뉴스 건너뛰기: {date} - {title_text}")
                    continue

                unique_titles.add(clean_title_text)
                unique_links.add(link)

                crawled_links.append({
                    "date": date,
                    "source": source,
                    "title": title_text,
                    "link": link
                })
                logger.debug(f"Added news: {date} - {title_text}")

            if stop_crawling:
                break

    return crawled_links
