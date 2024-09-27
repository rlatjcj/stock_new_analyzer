import asyncio
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from stock_news_analyzer.finder import get_news_link


@pytest.fixture
def mock_requests_get():
    with patch("stock_news_analyzer.finder.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_bs4():
    with patch("stock_news_analyzer.finder.BeautifulSoup") as mock_bs4:
        mock_soup = MagicMock()
        mock_items = []
        for i in range(5):  # 5개의 뉴스 항목 생성
            mock_item = MagicMock()
            mock_date_elem = MagicMock()
            mock_date_elem.get_text.return_value = (
                datetime.now() - timedelta(days=i)
            ).strftime("%Y.%m.%d %H:%M")
            mock_info_elem = MagicMock()
            mock_info_elem.get_text.return_value = f"Test Source {i}"
            mock_title_elem = MagicMock()
            mock_title_elem.get_text.return_value = f"Test Title {i}"
            mock_link_elem = MagicMock()
            mock_link_elem.get.return_value = f"/test_link_{i}"
            mock_title_elem.find.return_value = mock_link_elem
            mock_item.select_one.side_effect = [mock_date_elem, mock_info_elem, mock_title_elem]
            mock_items.append(mock_item)
        mock_soup.select.return_value = mock_items
        mock_bs4.return_value = mock_soup
        yield mock_bs4


def test_get_news_link_with_code(mock_requests_get, mock_bs4):
    result = asyncio.run(get_news_link(code="000660"))
    assert result is not None
    assert len(result) == 5
    assert result[0]["title"] == "Test Title 0"
    assert result[0]["link"] == "https://finance.naver.com/test_link_0"


def test_get_news_link_with_company(mock_requests_get, mock_bs4):
    result = asyncio.run(get_news_link(company="삼성전자"))
    assert result is not None
    assert len(result) == 5
    assert result[0]["title"] == "Test Title 0"
    assert result[0]["link"] == "https://finance.naver.com/test_link_0"


def test_get_news_link_with_date_range(mock_requests_get, mock_bs4):
    result = asyncio.run(get_news_link(code="000660", date_from="2023.05.01", date_to="2023.05.31"))
    assert result is not None
    assert len(result) == 5
    assert result[0]["title"] == "Test Title 0"
    assert result[0]["link"] == "https://finance.naver.com/test_link_0"


def test_get_news_link_max_pages(mock_requests_get, mock_bs4):
    result = asyncio.run(get_news_link(code="000660", max_pages=3))
    assert result is not None
    assert len(result) == 5
    assert result[0]["title"] == "Test Title 0"
    assert result[0]["link"] == "https://finance.naver.com/test_link_0"


def test_get_news_link_error_handling(mock_requests_get):
    mock_requests_get.side_effect = Exception("Test error")
    with pytest.raises(Exception):
        asyncio.run(get_news_link(code="000660"))
