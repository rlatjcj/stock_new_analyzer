import argparse
import asyncio
import logging
from datetime import datetime

from dotenv import load_dotenv

from stock_news_analyzer.finder import get_news_list
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


def main() -> None:
    load_dotenv()
    args = get_arguments()
    setup_logging(args.log_level)

    news_links = asyncio.run(get_news_list(  # noqa: F841
        company=args.company,
        date_from=args.date_from,
        date_to=args.date_to,
        max_pages=args.max_pages
    ))


if __name__ == "__main__":
    main()
