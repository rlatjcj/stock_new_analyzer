from datetime import datetime

from dotenv import load_dotenv

from stock_news_analyzer.finder import get_news_link


def main() -> None:
    # 사용자 입력 받기
    company_input = input("회사 코드 또는 이름을 입력하세요: ")
    # 날짜 입력 받기 (기본값은 오늘 날짜)
    today = datetime.now().strftime("%Y.%m.%d")
    date_from = input(f"시작 날짜를 입력하세요 (YYYY.MM.DD 형식, 기본값: {today}): ") or today
    date_to = input(f"종료 날짜를 입력하세요 (YYYY.MM.DD 형식, 기본값: {today}): ") or today

    # 날짜 형식 검증
    date_format = "%Y.%m.%d"
    if date_from:
        try:
            datetime.strptime(date_from, date_format)
        except ValueError:
            print("잘못된 시작 날짜 형식입니다. YYYY.MM.DD 형식으로 입력해주세요.")
            return

    if date_to:
        try:
            datetime.strptime(date_to, date_format)
        except ValueError:
            print("잘못된 종료 날짜 형식입니다. YYYY.MM.DD 형식으로 입력해주세요.")
            return

    # 회사 코드인지 이름인지 확인
    if company_input.isdigit():
        news_links = get_news_link(code=company_input, date_from=date_from, date_to=date_to)
    else:
        news_links = get_news_link(company=company_input, date_from=date_from, date_to=date_to)

    if news_links:
        print(f"총 {len(news_links)}개의 뉴스 링크를 찾았습니다:")
        for news in news_links:
            print(f"[{news['date']}] {news['title']} - {news['link']}")
    else:
        print("뉴스 링크를 찾을 수 없습니다.")


if __name__ == "__main__":
    load_dotenv()
    main()
