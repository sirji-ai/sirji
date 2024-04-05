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

`sirji-agents` is a PyPI package that implements three key agents for Sirji:

- Coding Agent
- Planning Agent
- Research Agent

It Utilizes:

- OpenAI Chat Completions API
- OpenAI Assistants API

This package communicates with models and RAG assistants.

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
export SIRJI_WORKSPACE="Absolute folder path for Sirji to use as it's workspace. Note that a .sirji folder will be created inside it."
export SIRJI_RUN_ID='Unique alphanumeric ID for each run. Note that a sub folder named by this ID will be created inside of .sirji folder to store logs, etc.'
export SIRJI_OPENAI_API_KEY='OpenAI API key for Chat Completions API and Assistants API'
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

researcher.message(message_str)
```

### Coding Agent

```python
from sirji_agents import CodingAgent

# Initialize Coding Agent
coder = CodingAgent()

# Construct a message for problem statement
from sirji_messages import MessageFactory, ActionEnum
message_class = MessageFactory[ActionEnum.PROBLEM_STATEMENT.name]
message_str = message_class().generate({"details": "Create a python executable file to find out the factorial of a number"})

# At the beginning, history is empty
coder_history = []

# call the Coder and update the history variable
response_message, coder_history = coder.message(message_str, coder_history)

# Now in the new history:
# coder_history[0] is the system prompt
# coder_history[1] is the message from User to Coder passing the problem statement
# coder_history[2] is the response from the LLM inference

# Persist the history variable for future use.
```

### Planning Agent

```python
from sirji_agents import PlanningAgent

# Initialize Planning Agent
planner = PlanningAgent()

# Construct a message for generate steps message
from sirji_messages import MessageFactory, ActionEnum
message_class = MessageFactory[ActionEnum.GENERATE_STEPS.name]
message_str = message_class().generate({"details": "Create a python executable file to find out the factorial of a number"})

# In the actual flow, this message_str will be obtained as a response from Coder.

# At the beginning, history is empty
planner_history = []

# call the Planner and update the history variable
response_message, planner_history = planner.message(message_str, planner_history)
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
