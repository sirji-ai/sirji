from .base import BaseContentHandler
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from sirji.tools.logger import researcher as logger

class WebPageHandler(BaseContentHandler):
    def handle(self, url, output_dir):
        logger.info(f"Researcher: Handling web page URL: {url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Consider selecting a specific part of the HTML if needed
            # For example: main_content = soup.find('main')
            # Then, convert that part to Markdown
            markdown_content = md(str(soup), heading_style="ATX")
            self.save_content(markdown_content, url, output_dir, 'md')
        else:
            logger.error(f"Error fetching {url}: Status code {response.status_code}")
