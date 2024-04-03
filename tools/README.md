# sirji-tools

`sirji-tools` is a Python package.

## Installation

Install `sirji-tools` quickly with pip:

```
pip install sirji-tools
```

## Usage

### Crawl URLs 

Crawl URLs tool will be used to crawl the web pages and extract the information from the web pages. And store the information for the further processing by researcher.

```python
from sirji_tools import crawl_urls

urls = ['https://www.google.com', 'https://www.yahoo.com']

crawl_urls(urls, 'workspace/researcher')
```

### Search 

Search tool will be used to search the information from the web pages based on the search terms provided. 
It returns the list of URLs related to the search terms.

```python
from sirji_tools import search_for

search_term = 'python programming'

urls = search_for(search_term)
```

### Logger

Logger tool will be used to log the information in the log file. It will be used to log the information to show the progress of the execution.

```python
from sirji_tools.logger import p_logger

p_logger.info("Log line here")
```

## License

`sirji-tools` is made available under the MIT License. See the included LICENSE file for more details.
