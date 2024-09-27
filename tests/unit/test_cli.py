from unittest.mock import patch

import pytest

from stock_news_analyzer.cli import main


@pytest.fixture
def mock_get_news_link():
    with patch("stock_news_analyzer.cli.get_news_link") as mock_get_news_link:
        yield mock_get_news_link


@pytest.fixture
def mock_filter_similar_news():
    with patch("stock_news_analyzer.cli.filter_similar_news") as mock_filter:
        yield mock_filter


@pytest.fixture
def mock_load_llm():
    with patch("stock_news_analyzer.cli.load_llm") as mock_load:
        yield mock_load


def test_main_with_company_code(mock_get_news_link, mock_filter_similar_news, mock_load_llm, capsys):
    mock_get_news_link.return_value = [
        {"date": "2023.05.01", "title": "Test News", "link": "https://test.com"}
    ]
    mock_filter_similar_news.return_value = mock_get_news_link.return_value

    with patch("sys.argv", ["stock-news-analyzer", "-c", "000660"]):
        result = main()

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["title"] == "Test News"


def test_main_with_company_name(mock_get_news_link, mock_filter_similar_news, mock_load_llm, capsys):
    mock_get_news_link.return_value = [
        {"date": "2023.05.01", "title": "Test News", "link": "https://test.com"}
    ]
    mock_filter_similar_news.return_value = mock_get_news_link.return_value

    with patch("sys.argv", ["stock-news-analyzer", "-c", "삼성전자"]):
        result = main()

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["title"] == "Test News"


def test_main_with_date_range(mock_get_news_link, mock_filter_similar_news, mock_load_llm, capsys):
    mock_get_news_link.return_value = [
        {"date": "2023.05.15", "title": "Test News", "link": "https://test.com"}
    ]
    mock_filter_similar_news.return_value = mock_get_news_link.return_value

    with patch("sys.argv", ["stock-news-analyzer", "-c", "000660", "-f", "2023.05.01", "-t", "2023.05.31"]):
        result = main()

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["date"] == "2023.05.15"


def test_main_no_news_found(mock_get_news_link, mock_filter_similar_news, mock_load_llm, capsys):
    mock_get_news_link.return_value = []
    mock_filter_similar_news.return_value = []

    with patch("sys.argv", ["stock-news-analyzer", "-c", "000660"]):
        result = main()

    assert isinstance(result, list)
    assert len(result) == 0


def test_main_invalid_date_format(capsys):
    with patch("sys.argv", ["stock-news-analyzer", "-c", "000660", "-f", "2023-05-01"]):
        result = main()

    assert isinstance(result, list)
    assert len(result) == 0
    captured = capsys.readouterr()
    assert "잘못된 날짜 형식입니다" in captured.err


def test_main_with_valid_arguments(mock_get_news_link, mock_filter_similar_news, mock_load_llm):
    mock_get_news_link.return_value = [
        {"date": "2023.05.01", "title": "Test News 1", "link": "https://test1.com"},
        {"date": "2023.05.02", "title": "Test News 2", "link": "https://test2.com"}
    ]
    mock_filter_similar_news.return_value = mock_get_news_link.return_value

    with patch("sys.argv", ["stock-news-analyzer", "-c", "000660", "-m", "gpt-4"]):
        result = main()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["title"] == "Test News 1"
    assert result[1]["title"] == "Test News 2"

# 다른 테스트 케이스들도 비슷하게 수정
