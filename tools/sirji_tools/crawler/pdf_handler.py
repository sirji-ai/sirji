from .base import BaseContentHandler
import os
import requests
import PyPDF2
from markdownify import markdownify as md
from sirji_tools.logger import create_logger

class PDFHandler(BaseContentHandler):
    def handle(self, url, output_dir):
        logger = create_logger("researcher.log", "debug")
        logger.info(f"Started crawling PDF from URL: {url}")

        response = requests.get(url)
        temp_pdf_path = os.path.join(output_dir, 'temp.pdf')
        
        with open(temp_pdf_path, 'wb') as f:
            f.write(response.content)
        try:
            with open(temp_pdf_path, 'rb') as pdf_file:
                logger.info(f"Reading PDF file content")
                reader = PyPDF2.PdfReader(pdf_file)
                text_content = '\n'.join(page.extract_text() for page in reader.pages if page.extract_text())

            logger.info(f"Converting PDF content to markdown")
            markdown_content = md(text_content)
            logger.info(f"Saving markdown content to file")
            self.save_content(markdown_content, url, output_dir, 'md')
        
        except Exception as e:
            logger.error(f"Failed to convert PDF to markdown: {e}")
        
        finally:
            os.remove(temp_pdf_path)
            logger.info(f"Completed crawling PDF from URL: {url}")
