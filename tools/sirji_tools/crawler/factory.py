import re
from .web_page_handler import WebPageHandler
from .pdf_handler import PDFHandler
from .github_handler import GitHubHandler
from sirji_tools.logger import create_logger

class ContentHandlerFactory:
    @classmethod
    def get_handler(cls, url):
        logger = create_logger("researcher.log", "debug")
        logger.info(f"Getting crawler handler for URL: {url}")

        if url.endswith('.pdf'):
            return PDFHandler()
        # elif 'github.com' in url:
        #     # Check if URL follows the pattern of a GitHub repo main page
        #     if re.match(r'^https://github\.com/[\w-]+/[\w-]+/?$', url):
        #         return GitHubHandler()
        #     else:
        #         logger.info(f"URL {url} does not match GitHub repository pattern. Crawling as a web page.")
        #         return WebPageHandler()
        else:
            return WebPageHandler()

# Example usage:
# handler = ContentHandlerFactory.get_handler(url)
# handler.handle(url, output_dir)
