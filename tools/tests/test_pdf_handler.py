import pytest
from unittest.mock import patch, MagicMock
from sirji_tools.crawler.pdf_handler import PDFHandler

class TestPDFHandler:
    @patch('sirji_tools.crawler.pdf_handler.requests.get')
    @patch('sirji_tools.crawler.pdf_handler.PyPDF2.PdfReader')
    def test_handle_pdf_success(self, mock_pdf_reader, mock_get, tmp_path):
        # Setup
        # Mocking the response of requests.get to simulate downloading a PDF
        mock_response = MagicMock()
        mock_response.content = b'PDF content'
        mock_get.return_value = mock_response

        # Mocking PyPDF2 to simulate reading a PDF file
        mock_pdf_instance = MagicMock()
        mock_pdf_instance.pages = [MagicMock(extract_text=MagicMock(return_value="Page text"))]
        mock_pdf_reader.return_value = mock_pdf_instance

        # Test data
        url = 'https://example.com/test.pdf'
        output_dir = tmp_path / "test_output"
        output_dir.mkdir()  # Ensure the directory exists

        # Execute the function under test
        handler = PDFHandler()
        handler.handle(url, str(output_dir))  # Convert Path object to string if necessary

        # Assertions
        mock_get.assert_called_once_with(url)
        mock_pdf_reader.assert_called_once()
        # Additional assertions can be added here to verify the content was saved correctly

    @patch('sirji_tools.crawler.pdf_handler.requests.get')
    def test_handle_pdf_network_failure(self, mock_get, tmp_path):
        # Setup
        # Simulating a network failure during PDF download
        mock_get.side_effect = Exception("Network failure")

        # Test data
        url = 'https://example.com/failing_url.pdf'
        output_dir = tmp_path / "test_output"
        output_dir.mkdir()  # Ensure the directory exists

        # Execute the function under test
        handler = PDFHandler()

        # Assertions
        with pytest.raises(Exception) as exc_info:
            handler.handle(url, str(output_dir))  # Convert Path object to string if necessary
        assert str(exc_info.value) == "Network failure", "PDFHandler did not handle network failure as expected."