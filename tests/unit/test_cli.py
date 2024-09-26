import asyncio
from unittest.mock import patch

import pytest

from stock_news_analyzer.cli import main


@pytest.fixture
def mock_input():
    with patch("builtins.input") as mock_input:
        yield mock_input

@pytest.fixture
def mock_get_news_link():
    with patch("stock_news_analyzer.cli.get_news_link") as mock_get_news_link:
        yield mock_get_news_link

def test_main_with_company_code(mock_input, mock_get_news_link, capsys):
    mock_input.side_effect = ["000660", "", ""]
    mock_get_news_link.return_value = [
        {"date": "2023.05.01", "title": "Test News", "link": "https://test.com"}
    ]

    asyncio.run(main())

    captured = capsys.readouterr()
    assert "총 1개의 뉴스 링크를 찾았습니다:" in captured.out
    assert "[2023.05.01] Test News - https://test.com" in captured.out

def test_main_with_company_name(mock_input, mock_get_news_link, capsys):
    mock_input.side_effect = ["삼성전자", "", ""]
    mock_get_news_link.return_value = [
        {"date": "2023.05.01", "title": "Test News", "link": "https://test.com"}
    ]

    asyncio.run(main())

    captured = capsys.readouterr()
    assert "총 1개의 뉴스 링크를 찾았습니다:" in captured.out
    assert "[2023.05.01] Test News - https://test.com" in captured.out

def test_main_with_date_range(mock_input, mock_get_news_link, capsys):
    mock_input.side_effect = ["000660", "2023.05.01", "2023.05.31"]
    mock_get_news_link.return_value = [
        {"date": "2023.05.15", "title": "Test News", "link": "https://test.com"}
    ]

    asyncio.run(main())

    captured = capsys.readouterr()
    assert "총 1개의 뉴스 링크를 찾았습니다:" in captured.out
    assert "[2023.05.15] Test News - https://test.com" in captured.out

def test_main_no_news_found(mock_input, mock_get_news_link, capsys):
    mock_input.side_effect = ["000660", "", ""]
    mock_get_news_link.return_value = None

    asyncio.run(main())

    captured = capsys.readouterr()
    assert "뉴스 링크를 찾을 수 없습니다." in captured.out

def test_main_invalid_date_format(mock_input, capsys):
    mock_input.side_effect = ["000660", "2023-05-01", ""]

    asyncio.run(main())

    captured = capsys.readouterr()
    assert "잘못된 시작 날짜 형식입니다. YYYY.MM.DD 형식으로 입력해주세요." in captured.out
