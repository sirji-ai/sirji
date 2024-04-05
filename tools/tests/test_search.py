import pytest
from unittest.mock import patch, MagicMock  # Updated import here
from sirji_tools.search import search_for

@patch('sirji_tools.search.search.sync_playwright')
def test_search_for_returns_filtered_urls(mock_playwright):
    # Setup the mock environment
    mock_browser_context = mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value.new_context.return_value
    mock_browser_page = mock_browser_context.new_page.return_value
    
    # Mocking the navigation to Google's search page
    mock_browser_page.goto.return_value = None
    
    # Mocking the filling and pressing enter on the search input
    mock_browser_page.fill.return_value = None
    mock_browser_page.press.return_value = None
    
    # Simulate a delay for loading search results
    # skipping the time.sleep through mock
    
    # Mocking the query_selector_all method to return mock links as search results
    mock_browser_page.query_selector_all.return_value = [
        MagicMock(get_attribute=MagicMock(return_value='https://www.google.com/url?url=https://www.example.com')),
        MagicMock(get_attribute=MagicMock(return_value='https://www.google.com/url?url=https://www.maps.google.com')),
        MagicMock(get_attribute=MagicMock(return_value='https://www.google.com/url?url=https://www.example2.com')),
        # Add more mock results as needed
    ]
    
    expected_urls = ['https://www.example.com', 'https://www.example2.com']  # Expected output after filtering excluded domains and duplicates
    actual_urls = search_for('test query')
    
    # Assertions
    assert len(actual_urls) <= 10, "The function returned more than 10 URLs."
    assert set(expected_urls).issubset(set(actual_urls)), "The returned URLs are not as expected after filtering."
    mock_browser_page.goto.assert_called_once_with('https://www.google.com')
    mock_browser_page.fill.assert_called_once_with('input[name=q]', 'test query')
    mock_browser_page.press.assert_called_once_with('input[name=q]', 'Enter')