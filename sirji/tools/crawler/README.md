
# Crawler Module

The Crawler module in the Sirji project is designed to process a list of URLs and handle different types of content such as web pages, PDFs, and GitHub repositories. It utilizes a factory pattern to select the appropriate handler based on the URL's content type.

## Handlers

- **WebPageHandler**: Crawls web page URLs and saves the content in markdown format.
- **PDFHandler**: Downloads PDFs from URLs, converts them to markdown format, and saves the content.
- **GitHubHandler**: Clones GitHub repositories from provided URLs.

## Usage

To use the crawler module, you need to pass a list of URLs and an output directory where the crawled content will be saved.

```python
from sirji.tools.crawler import crawl_urls

urls = [
    'http://example.com',
    'https://github.com/user/repository',
    'http://example.com/document.pdf'
]

output_dir = 'path/to/output/directory'

crawl_urls(urls, output_dir)
```

This will process each URL using the appropriate handler and save the content in the specified output directory.

## Installation

Ensure you have all the dependencies installed by running:

```bash
pip install -r requirements.txt
```

This module relies on external libraries such as `playwright` for web crawling, `PyPDF2` and `markdownify` for PDF processing, and standard Python libraries for handling GitHub repositories.