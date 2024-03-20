# Setup Steps

# Virtual Environment

Create a virtual environment to separate Python dependencies, allowing for project-specific packages without interfering with system-wide installations.

```zsh
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```zsh
pip install -r requirements.txt
```

## Setup Environment Variables

```zsh
export SIRJI_OPENAI_API_KEY='YOUR OPENAI API KEY'
```

## Example Usages

TODO: remove the following section later when main process is ready.
### Researcher

```python
from sirji.agents.researcher import Researcher

# Initialize Researcher
researcher = Researcher('openai_assistant', 'openai_assistant')

# For given URLs, convert to markdown files. Generate and store embeddings.
researcher.index(['https://example.com'])

# Retrieve the matching context uisng embeddings and pass it along prompt for inference.
researcher.infer('Sample question')
```
