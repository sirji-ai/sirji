# Setup Steps

## Virtual Environment

Create a virtual environment to separate Python dependencies, allowing for project-specific packages without interfering with system-wide installations.

```zsh
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```zsh
pip install -r requirements.txt
playwright install
```

## Setup Environment Variables

```zsh
export SIRJI_OPENAI_API_KEY='OPENAI API KEY'
export SIRJI_GOOGLE_SEARCH_API_KEY='GOOGLE SEARCH API KEY'
export SIRJI_GOOGLE_SEARCH_ENGINE_ID='GOOGLE SEARCH ENGINE ID'
```

## Start Sirji

```zsh
python3 main.py
```
