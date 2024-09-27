import argparse
import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List

from dotenv import load_dotenv

from stock_news_analyzer.finder import get_news_link
from stock_news_analyzer.model import get_available_models

logger = logging.getLogger(__name__)


def setup_logging(log_level: str) -> None:
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="주식 뉴스 분석기")
    parser.add_argument("-c", "--company", required=True, help="회사 코드 또는 이름")
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
    parser.add_argument(
        "-p", "--max_pages",
        help="크롤링할 최대 페이지 수",
        type=int,
        default=5
    )
    parser.add_argument(
        "--log-level",
        help="로깅 레벨",
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO'
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


async def get_news_list(args: argparse.Namespace) -> List[Dict[str, Any]]:
    # 날짜 형식 검증
    if not all(inspect_date_format(date) for date in [args.date_from, args.date_to]):
        return []

    logger.info(f"뉴스 검색 시작: 회사 - {args.company}, 기간 - {args.date_from} ~ {args.date_to}")

    # 해당 날짜의 뉴스 가져오기
    news_links: List[Dict[str, Any]] = await get_news_link(
        code=args.company if args.company.isdigit() else None,
        company=args.company if not args.company.isdigit() else None,
        date_from=args.date_from,
        date_to=args.date_to,
        max_pages=args.max_pages
    )

    logger.info(f"총 {len(news_links)}개의 뉴스를 찾았습니다.")

    # LLM 모델 로드 (필요한 경우 사용)
    # llm = load_llm(args.model)
    # logger.info(f"LLM 모델 '{args.model}'을 로드했습니다.")

    if news_links:
        logger.info(f"총 {len(news_links)}개의 뉴스 링크를 찾았습니다:")
        for news in news_links:
            logger.info(f"[{news['date']}] {news['title']} - {news['link']}")
    else:
        logger.info("뉴스 링크가 없습니다.")

    return news_links


def main() -> List[Dict[str, Any]]:
    load_dotenv()
    args = get_arguments()
    setup_logging(args.log_level)
    return asyncio.run(get_news_list(args))


if __name__ == "__main__":
    main()
