<p align="center">
  <a href="." target="blank"><img src="https://github.com/sirji-ai/sirji/assets/7627517/363fc6dd-69af-4d84-8b7c-a91ec092058d" width="250" alt="Sirji Logo" /></a>
</p>

<p align="center">
  <em>Sirji is an agentic AI framework for software development.</em>
</p>

<p align="center">
  Built with ❤️ by <a href="https://truesparrow.com/" target="_blank">True Sparrow</a>
</p>

<p align="center">
  <img alt="GitHub License" src="https://img.shields.io/github/license/sirji-ai/sirji">
  <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/sirji-ai/sirji">
  <img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues/sirji-ai/sirji">
  <img alt="PyPI sirji-tools" src="https://img.shields.io/pypi/v/sirji-tools.svg">
</p>

<p align="center">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/sirji-ai/sirji">
  <img alt="GitHub forks" src="https://img.shields.io/github/forks/sirji-ai/sirji">
  <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/sirji-ai/sirji">
</p>

## Sirji Tools

`sirji-tools` is a PyPI package that provides tools for:

- Crawling (downloading web pages to markdown files)
- Searching on Google
- Custom Logging

## Installation

### Setup Virtual Environment

We recommend setting up a virtual environment to isolate Python dependencies, ensuring project-specific packages without conflicting with system-wide installations.

```zsh
python3 -m venv venv
source venv/bin/activate
```

### Install Package

Install the package from PyPi:

```zsh
pip install sirji-tools
```

Run the following command to install playwright:

```zsh
playwright install
```

## Usage

### Environment Variables

Ensure that the following environment variables are set:

```zsh
export SIRJI_PROJECT="Absolute folder path for Sirji to use as its project folder."
export SIRJI_RUN_PATH='Folder having run specific logs, etc.'
```

### Crawl URLs

Crawl URLs tool will be used to crawl the web pages and extract the information from the web pages. And store the information for further processing by the researcher.

```python
from sirji_tools import crawl_urls

urls = ['https://www.google.com', 'https://www.yahoo.com']

crawl_urls(urls, 'project/researcher')
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

## For Contributors

1. Fork and clone the repository.
2. Create and activate the virtual environment as described above.
3. Set the environment variables as described above.
4. Install the package in editable mode by running the following command from the repository root:

```zsh
pip install -e .
```

5. Run the following command to install playwright:

```zsh
playwright install
```

## Running Tests and Coverage Analysis

Follow the above-mentioned steps for "contributors", before running the test cases.

```zsh
# Install testing dependencies
pip install pytest coverage

# Execute tests
pytest

# Measure coverage, excluding test files
coverage run --omit="tests/*" -m pytest
coverage report
```

## License

Distributed under the MIT License. See `LICENSE` for more information.
