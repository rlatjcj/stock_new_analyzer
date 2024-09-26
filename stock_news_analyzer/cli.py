import argparse
import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List

from dotenv import load_dotenv

from stock_news_analyzer.filter import filter_similar_news
from stock_news_analyzer.finder import get_news_link
from stock_news_analyzer.model import get_available_models, load_llm

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="주식 뉴스 분석기")
    parser.add_argument("company", help="회사 코드 또는 이름")
    parser.add_argument(
        "-f", "--date_from",
        help="시작 날짜 (YYYY.MM.DD 형식)",
        default=datetime.now().strftime("%Y.%m.%d")
    )
    parser.add_argument(
        "-t", "--date_to",
        help="종료 날짜 (YYYY.MM.DD 형식)",
        default=datetime.now().strftime("%Y.%m.%d")
    )
    parser.add_argument(
        "-m", "--model",
        help="사용할 LLM 모델",
        choices=get_available_models(),
        default="gpt-3.5-turbo"
    )
    return parser.parse_args()


def inspect_date_format(date_str: str) -> bool:
    date_format = "%Y.%m.%d"
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        logger.error(f"잘못된 날짜 형식입니다: {date_str}. YYYY.MM.DD 형식으로 입력해주세요.")
        return False


async def main() -> None:
    args = get_arguments()

    # 날짜 형식 검증
    if not all(inspect_date_format(date) for date in [args.date_from, args.date_to]):
        return

    logger.info(f"뉴스 검색 시작: 회사 - {args.company}, 기간 - {args.date_from} ~ {args.date_to}")

    # 해당 날짜의 뉴스 가져오기
    news_links: List[Dict[str, Any]] = await get_news_link(
        code=args.company if args.company.isdigit() else None,
        company=args.company if not args.company.isdigit() else None,
        date_from=args.date_from,
        date_to=args.date_to
    )

    logger.info(f"총 {len(news_links)}개의 뉴스를 찾았습니다.")

    # LLM 모델 로드
    llm = load_llm(args.model)
    logger.info(f"LLM 모델 '{args.model}'을 로드했습니다.")

    # 유사한 뉴스 필터링
    filtered_news = filter_similar_news(news_links, llm)

    if filtered_news:
        logger.info(f"총 {len(filtered_news)}개의 필터링된 뉴스 링크를 찾았습니다:")
        for news in filtered_news:
            logger.info(f"[{news['date']}] {news['title']} - {news['link']}")
    else:
        logger.info("필터링된 뉴스 링크가 없습니다.")

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
