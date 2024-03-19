from .base import BaseContentHandler
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

class WebPageHandler(BaseContentHandler):
    def handle(self, url, output_dir):
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Consider selecting a specific part of the HTML if needed
            # For example: main_content = soup.find('main')
            # Then, convert that part to Markdown
            markdown_content = md(str(soup), heading_style="ATX")
            self.save_content(markdown_content, url, output_dir, 'md')
        else:
            print(f"Error fetching {url}: Status code {response.status_code}")
