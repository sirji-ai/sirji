<p align="center">
  <a href="." target="blank"><img src="https://github.com/sirji-ai/sirji/assets/7627517/363fc6dd-69af-4d84-8b7c-a91ec092058d" width="250" alt="Sirji Logo" /></a>
</p>

<p align="center">
  <em>Sirji is an Open Source AI Software Development Agent.</em>
</p>

<p align="center">
  Built with :heart: by <a href="https://truesparrow.com/" target="_blank">True Sparrow</a>
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

```
pip install sirji-tools
```

## Usage

### Environment Variables

Ensure that following environment variables are set:

```zsh
export SIRJI_WORKSPACE="Absolute folder path for Sirji to use as it's workspace. Note that a .sirji folder will be created inside it."
export SIRJI_RUN_ID='Unique alphanumeric ID for each run. Note that a sub folder named by this ID will be created inside of .sirji folder to store logs, etc.'
```

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

## For Contributors

1. Fork and clone the repository.
2. Create and activate the virtual environment as described above.
3. Set the environment variables as described above.
4. Install the package in editable mode by running the following command from repository root:

```zsh
pip install -e .
```

## Running Tests and Coverage Analysis

Tests can be run, and coverage can be analyzed in a few simple steps:

```bash
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
