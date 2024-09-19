import argparse
from datetime import datetime

from dotenv import load_dotenv

from stock_news_analyzer.finder import get_news_link


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
    return parser.parse_args()

def inspect_date_format(date_str: str) -> bool:
        date_format = "%Y.%m.%d"
        try:
            datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            print(f"잘못된 날짜 형식입니다: {date_str}. YYYY.MM.DD 형식으로 입력해주세요.")
            return False



def main() -> None:
    args = get_arguments()

    # 날짜 형식 검증
    if not all(inspect_date_format(date) for date in [args.date_from, args.date_to]):
        return

    news_links = get_news_link(
        code=args.company if args.company.isdigit() else None,
        company=args.company if not args.company.isdigit() else None,
        date_from=args.date_from,
        date_to=args.date_to
    )

    if news_links:
        print(f"총 {len(news_links)}개의 뉴스 링크를 찾았습니다:")
        for news in news_links:
            print(f"[{news['date']}] {news['title']} - {news['link']}")
    else:
        print("뉴스 링크를 찾을 수 없습니다.")


if __name__ == "__main__":
    load_dotenv()
    main()
