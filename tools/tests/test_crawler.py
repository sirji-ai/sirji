import pytest
from unittest.mock import patch, MagicMock
from sirji_tools.crawler import crawl_urls
from sirji_tools.crawler.factory import ContentHandlerFactory

class TestCrawler:
    @patch('sirji_tools.crawler.factory.ContentHandlerFactory.get_handler')
    def test_crawl_urls_with_mock_handlers(self, mock_get_handler):
        # Setup
        # Mocking the handler to simulate handling URLs without actual network operations
        mock_handler = MagicMock()
        mock_get_handler.return_value = mock_handler

        # Test data
        urls = ['https://example.com/page1', 'https://example.com/page2']
        output_dir = 'test_output'

        # Execute the function under test
        crawl_urls(urls, output_dir)

        # Assertions
        assert mock_get_handler.call_count == len(urls), "get_handler was not called the expected number of times."
        mock_handler.handle.assert_called()
        assert mock_handler.handle.call_count == len(urls), "URL handler's handle method was not called the expected number of times."

    @patch('sirji_tools.crawler.web_page_handler.WebPageHandler.handle')
    def test_crawl_urls_with_specific_handler(self, mock_handle):
        # Setup
        # No need to mock get_handler here since we're directly testing with a specific handler type
        urls = ['https://example.com/page1']
        output_dir = 'test_output'

        # Execute the function under test with a setup that would use the WebPageHandler
        crawl_urls(urls, output_dir)

        # Assertions
        mock_handle.assert_called_once_with(urls[0], output_dir), "WebPageHandler's handle method was not called as expected."
