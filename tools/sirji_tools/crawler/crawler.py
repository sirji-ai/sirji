from .factory import ContentHandlerFactory
from sirji_tools.logger import r_logger as logger


def crawl_urls(urls, output_dir):
    """
    Processes a list of URLs using the appropriate handlers based on the URL type.
    - urls: A list of URLs to process.
    - output_dir: The directory where output from the handlers should be stored.
    """
    for url in urls:
        logger.info(f"Started crawling URL: {url}")

        handler = ContentHandlerFactory.get_handler(url)

        try:
            handler.handle(url, output_dir)
            logger.info(f"Completed crawling URL: {url}")
        except Exception as e:
            logger.info(f"Crawling failed for URL: {url}")
