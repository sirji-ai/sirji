from playwright.sync_api import sync_playwright
import time
from markdownify import markdownify as md
import re

from .base import BaseContentHandler
from sirji_tools.logger import create_logger


class WebPageHandler(BaseContentHandler):
    def handle(self, url, output_dir):
        with sync_playwright() as pw:
            delay_seconds = 10

            logger = create_logger("researcher.log", "debug")
            logger.info(f"Started crawling web page URL: {url}")
            browser = pw.chromium.launch()

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            )
            page = context.new_page()

            page.goto(url, timeout=120000)

            time.sleep(delay_seconds)


            # Extract the content from the webpage body only
            body_content = page.query_selector('body').inner_html()

            # Remove script tags
            body_content = re.sub(r'<script.*?</script>',
                                  '', body_content, flags=re.DOTALL)

            # Convert the content to markdown format
            markdown_content = md(body_content)

            self.save_content(markdown_content, url, output_dir, 'md')

            browser.close()

            logger.info(f"Completed crawling web page URL: {url}")
