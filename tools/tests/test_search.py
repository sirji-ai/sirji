import pytest
from unittest.mock import patch, MagicMock
from sirji_tools.search import search_for

class TestSearch:
    @patch('sirji_tools.search.search.requests.get')
    @patch('sirji_tools.search.search.load_config')
    def test_search_for_success(self, mock_load_config, mock_get):
        # Setup
        # Mocking load_config to return a predefined configuration
        mock_load_config.return_value = {
            'google_search_url': 'https://www.googleapis.com/customsearch/v1',
            'search_results_per_page': 10
        }

        # Mocking the response of requests.get
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'items': [
                {'link': 'https://example.com/page1'},
                {'link': 'https://example.com/page2'}
            ]
        }
        mock_get.return_value = mock_response

        # Expected result
        expected_urls = ['https://example.com/page1', 'https://example.com/page2']

        # Actual call
        result = search_for('test query')

        # Assertions
        assert result == expected_urls, "The search_for function did not return the expected URLs."

    @patch('sirji_tools.search.search.requests.get')
    @patch('sirji_tools.search.search.load_config')
    def test_search_for_failure(self, mock_load_config, mock_get):
        # Setup
        # Mocking load_config to return a predefined configuration
        mock_load_config.return_value = {
            'google_search_url': 'https://www.googleapis.com/customsearch/v1',
            'search_results_per_page': 10
        }

        # Simulating a network failure during the search
        mock_get.side_effect = Exception("Network failure")

        # Testing for exception handling
        with pytest.raises(Exception) as exc_info:
            search_for('test query')

        assert str(exc_info.value) == "Network failure", "The search_for function did not handle the exception as expected."

    @patch('sirji_tools.search.search.load_config')
    def test_search_for_empty_query(self, mock_load_config):
        # Setup
        # Mocking load_config to return a predefined configuration
        mock_load_config.return_value = {
            'google_search_url': 'https://www.googleapis.com/customsearch/v1',
            'search_results_per_page': 10
        }

        # Testing for empty query handling
        with pytest.raises(KeyError) as exc_info:
            search_for('')

        assert str(exc_info.value) == "'Query is empty'", "The search_for function did not handle the empty query as expected."