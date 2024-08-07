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
  <img alt="PyPI sirji-agents" src="https://img.shields.io/pypi/v/sirji-agents.svg">
</p>

<p align="center">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/sirji-ai/sirji">
  <img alt="GitHub forks" src="https://img.shields.io/github/forks/sirji-ai/sirji">
  <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/sirji-ai/sirji">
</p>

## Sirji Agents

`sirji-agents` is a PyPI package that implements the following components of the Sirji AI agentic framework:
- **Orchestrator**: The Orchestrator is the central component in the Sirji framework, responsible for managing the flow and execution of tasks across different agents.
- **Generic Agent**: Run time composable class providing the agent functionality as per the pseudo code provided in the agent.yml file.

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

Ensure that the following environment variables are set:

```zsh
export SIRJI_PROJECT="Absolute folder path for Sirji to use as its project folder."
export SIRJI_INSTALLATION_DIR='Absolute path of the Sirji installation directory.'
export SIRJI_RUN_PATH='Folder path containing run related logs, etc.'
export SIRJI_MODEL_PROVIDER='Model Provider to be used for LLM inference. Defaults to "openai".'
export SIRJI_MODEL='Model to be used for LLM inference. Defaults to "gpt-4o".'
export SIRJI_MODEL_PROVIDER_API_KEY='API key to be used for LLM inference.'
```

### Orchestrator

The Orchestrator is the central component in the Sirji framework, responsible for managing the flow and execution of tasks across different agents.

```python
from sirji_agents import Orchestrator

agent_output_folder_index = {
  "SIRJI/problem.txt": {
    "description": "Problem statement from the user.",
    "created_by": "SIRJI"
  },
  "PRODUCT_MANAGER/finalized_epics_user_stories.txt": {
    "description": "Finalized Epics and User Stories for the Tic-Tac-Toe game with AI opponent.",
    "created_by": "PRODUCT_MANAGER"
  },
  "ARCHITECT/finalized_architecture_components.txt": {
    "description": "Finalized architecture components for the Tic-Tac-Toe game with AI opponent.",
    "created_by": "ARCHITECT"
  }
}

agent = Orchestrator(agent_output_folder_index)

# History is the array of LLM conversations till now
history = []

# Input message string
message_str = ""
response_message, history, prompt_tokens, completion_tokens = agent.message(message_str, history)
```

### Generic Agent

Run time composable class providing the agent functionality as per the pseudo code provided in the agent.yml file.

```python
# Convert the agent.yml file to a Python dictionary
config = {
  "id": "CODER",
  "name": "Coding Agent",
  "llm": {
    "provider": "openai",
    "model": "gpt-4o"
  },
  "skill": "Developing end-to-end working code for the epic & user stories, making use of the finalized architecture components.",
  "pseudo_code": "1. Read the problem statement from the Agent Output Folder.\n2. Read the epics & user stories from the Agent Output Folder.\n3. Read the architecture components from the Agent Output Folder.\n4. Write concrete code implementing the epics & user stories and the problem statement, following these rules:\n   - Ensure that the code follows secure software development practices.\n   - The code files should be created inside the project folder.\n5. Install necessary packages or libraries in local folders.\n   - Check if the programming language-specific packages or libraries are already installed.\n   - If not installed, install using tools like venv for Python or package.json for Node.js.\n6. Verify system-level command installations.\n   - Confirm if required system-level commands are already installed by checking versions to avoid redundant installations.\n7. Execute the written code and evaluate the output.\n   - Run the code to check for any errors.\n   - If errors are found, solve them before proceeding.\n8. If the code requires a server, ensure to start or restart the server.\n   - Run commands compatible with SIRJI_OS.\n   - Use the command `npm start` or the relevant command to start the server."
}


agent_output_folder_index = {
  "SIRJI/problem.txt": {
    "description": "Problem statement from the user.",
    "created_by": "SIRJI"
  },
  "PRODUCT_MANAGER/finalized_epics_user_stories.txt": {
    "description": "Finalized Epics and User Stories for the Tic-Tac-Toe game with AI opponent.",
    "created_by": "PRODUCT_MANAGER"
  },
  "ARCHITECT/finalized_architecture_components.txt": {
    "description": "Finalized architecture components for the Tic-Tac-Toe game with AI opponent.",
    "created_by": "ARCHITECT"
  }
}

from sirji_agents import GenericAgent

agent = GenericAgent(config, agent_output_folder_index)

history = []
message_str = "***\nFROM: ORCHESTRATOR\nTO: CODER\nACTION: INVOKE_AGENT\nSUMMARY: Implement the epic & user stories using the architecture components.\nBODY:\nPImplement the epic & user stories using the architecture components.\n***"

response_message, history, prompt_tokens, completion_tokens = agent.message(message_str, history)
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

TODO - Introduce test cases.

## License

Distributed under the MIT License. See `LICENSE` for more information.
