<p align="center">
  <a href="." target="blank"><img src="https://github.com/sirji-ai/sirji/assets/7627517/363fc6dd-69af-4d84-8b7c-a91ec092058d" width="250" alt="Sirji Logo" /></a>
</p>

<p align="center">
  <em>Sirji is an Open Source AI Software Development Agent.</em>
</p>

<p align="center">
  Built with ❤️ by <a href="https://truesparrow.com/" target="_blank">True Sparrow</a>
</p>

<p align="center">
  <img alt="GitHub License" src="https://img.shields.io/github/license/sirji-ai/sirji">
  <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/sirji-ai/sirji">
  <img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues/sirji-ai/sirji">
  <img alt="PyPI sirji-agents" src="https://img.shields.io/pypi/v/sirji-agents.svg">
</p>

<p align="center">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/sirji-ai/sirji">
  <img alt="GitHub forks" src="https://img.shields.io/github/forks/sirji-ai/sirji">
  <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/sirji-ai/sirji">
</p>

## Sirji Agents

`sirji-agents` is a PyPI package that implements following components of the Sirji AI agentic framework:
- Orchestration Agent
- Research Agent
- Generic Agent

By default, it utilizes:
- OpenAI Chat Completions API
- OpenAI Assistants API

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
pip install sirji-agents
```

Run the following command to install playwright:

```zsh
playwright install
```

## Usage

### Environment Variables

Ensure that following environment variables are set:

```zsh
export SIRJI_WORKSPACE="Absolute folder path for Sirji to use as it's workspace."
export SIRJI_RUN_PATH='Folder path containing run related logs, etc.'
export SIRJI_OPENAI_API_KEY='OpenAI API key for Chat Completions API and Assistants API'
export SIRJI_MODEL_PROVIDER='Model Provider to be used for LLM inference. Defaults to "openai".'
export SIRJI_MODEL='Model to be used for LLM inference. Defaults to "gpt-4-turbo".'
export SIRJI_MODEL_PROVIDER_API_KEY='API key to be use for LLM inference.'
export SIRJI_INSTALLATION_DIR='Absolute path of the Sirji installation directory.'
```

### Orchestration Agent

```python
# Following is a sample recipe
recipe = {
  "prescribed_tasks": [
    "Write epics and user stories.",
    "Write architecture components.",
    "Implement the epic & user stories using the architecture components."
  ],
  "tips": [
    "Ensure finalized epics & user stories and architecture components are consistent. Address any discrepancies with the user."
  ]
}

# Following is a sample array of installed agents
installed_agents = [
  {
    "id": "PRODUCT_MANAGER",
    "name": "Product Manager Agent",
    "skills": [
      "Generation of epics and user stories for the problem statement."
    ]
  },
  {
    "id": "ARCHITECT",
    "name": "Architect Agent",
    "skills": [
      "Generation of architecture components."
    ]
  },
  {
    "id": "CODER",
    "name": "Coding Agent",
    "skills": [
      "Developing end-to-end working code for the epic & user stories, making use of the finalized architecture components."
    ]
  }
]

from sirji_agents import Orchestrator

agent = Orchestrator(recipe, installed_agents)

# History is the array of LLM conversation till now
history = []

# Input message string
message_str = ""
response_message, history, prompt_tokens, completion_tokens = agent.message(message_str, history)
```

### Generic Agent
```python
config = {
  "id": "CODER",
  "name": "Coding Agent",
  "llm": {
    "provider": "openai",
    "model": "gpt-4"
  },
  "skills": [
    {
      "skill": "Developing end-to-end working code for the epic & user stories, making use of the finalized architecture components.",
      "sub_tasks": [
        "Read problem statement, epics & user stories and architecture components from shared_resources.",
        "Write concrete code and not just conceptualize or outline or simulate it.",
        "Follow secure software development practices while generating code.",
        "Ensure that you don't create any file/folder outside of workspace root folder, i.e. './'",
        "Install programming language-specific packages or libraries in local folders, utilizing tools such as venv for installing Python dependencies and package.json for managing Node.js dependencies.",
        "Verify whether a system-level command is already installed to avoid triggering the installation of packages that are already in place.",
        "Always execute the code and evaluate the response output. If the response has errors, solve them before moving ahead."
      ]
    }
  ]
}

shared_resources_index = {
  "shared_resources/SIRJI/problem.txt": {
    "description": "Problem statement from the user.",
    "created_by": "SIRJI"
  },
  "shared_resources/PRODUCT_MANAGER/finalized_epics_user_stories.txt": {
    "description": "Finalized Epics and User Stories for the Tic-Tac-Toe game with AI opponent.",
    "created_by": "PRODUCT_MANAGER"
  },
  "shared_resources/ARCHITECT/finalized_architecture_components.txt": {
    "description": "Finalized architecture components for the Tic-Tac-Toe game with AI opponent.",
    "created_by": "ARCHITECT"
  }
}

from sirji_agents import GenericAgent

agent = GenericAgent(config, shared_resources_index)

history = []
message_str = "***\nFROM: ORCHESTRATOR\nTO: CODER\nACTION: INVOKE_AGENT\nSUMMARY: Implement the epic & user stories using the architecture components.\nBODY:\nPImplement the epic & user stories using the architecture components.\n***"

response_message, history, prompt_tokens, completion_tokens = agent.message(message_str, history)
```

### Research Agent

### Initialization

```python
from sirji_agents import ResearchAgent

# Initialize Researcher without assistant ID
researcher = ResearchAgent('openai_assistant', 'openai_assistant')

# init_payload fetched from researcher object should be persisted
init_payload = researcher.init_payload

# Initialize Researcher with assistant ID
researcher = ResearchAgent('openai_assistant', 'openai_assistant', init_payload)
```

Some example message handling usages are given below.

#### Train using URL

```python
from sirji_messages import MessageFactory, ActionEnum

message_class = MessageFactory[ActionEnum.TRAIN_USING_URL.name]
message_str = message_class().generate({"url": "https://finance.yahoo.com/quote/API/"})

researcher.message(message_str)
```

#### Infer

```python
from sirji_messages import MessageFactory, ActionEnum

message_class = MessageFactory[ActionEnum.INFER.name]
message_str = message_class().generate({"details": "How to use yahoo finance api?"})

response, total_tokens = researcher.message(message_str)
```

## For Contributors

1. Fork and clone the repository.
2. Create and activate the virtual environment as described above.
3. Set the environment variables as described above.
4. Install the package in editable mode by running the following command from repository root:

```zsh
pip install -e .
```

5. Run the following command to install playwright:

```zsh
playwright install
```

## Running Tests and Coverage Analysis

TODO

## License

Distributed under the MIT License. See `LICENSE` for more information.
