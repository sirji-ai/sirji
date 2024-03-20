# Setup Steps

## Install Dependencies

```zsh
pip install -r requirements.txt
```

## Setup Environment Variables

```zsh
export SIRJI_OPENAI_API_KEY='YOUR OPENAI API KEY'
```

## Example Usages

### Research Agent

```python
from sirji.agents.researcher import Researcher

# Initialize Researcher
researcher = Researcher('openai_assistant', 'openai_assistant')

# For given URLs, convert to markdown files. Generate and store embeddings.
researcher.index(['https://example.com'])

# Retrieve the matching context uisng embeddings and pass it along prompt for inference.
researcher.infer('Sample question')
```
