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
  <img alt="PyPI sirji-messages" src="https://img.shields.io/pypi/v/sirji-messages.svg">
</p>

<p align="center">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/sirji-ai/sirji">
  <img alt="GitHub forks" src="https://img.shields.io/github/forks/sirji-ai/sirji">
  <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/sirji-ai/sirji">
</p>

## Sirji Messages

`sirji-messages` is a PyPI package that implements the Sirji messaging protocol with the following highlights:

- **Message Factory**: A factory that provides a Message class for a given action.
- **Message Parser**: Parse structured message strings into Python dictionaries for easy access to the message components.
- **Allowed Response Templates**: Provides the part of the system prompt describing allowed Response Templates for a given agent pair.
- **Custom Exceptions**: A set of custom exceptions thrown by the message parser.
- **Enums for Agents and Actions**: Provides easy auto-completion while writing code.

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
pip install sirji-messages
```

## Usage

### Message Factory

A factory that provides a Message class for a given action.

```python
from sirji_messages import MessageFactory, ActionEnum

# Message class instantiation from an action enum
message_class = MessageFactory[ActionEnum.RESPONSE.name]
print(f"Sample RESPONSE message:\n{message_class().sample()}")

# Generate message using passed template variables
message_str = message_class().generate({
            "from_agent_id": "EXECUTOR",
            "to_agent_id": "CODER",
            "summary": "Empty",
            "body": "Done."})
            
print(f"Generated RESPONSE message:\n{message_str}")
```

### Message Parsing

Parse structured message strings into Python dictionaries for easy access to the message components.

````python
from sirji_messages import message_parse

# Example message string to parse
message_str = """***
FROM: EXECUTOR
TO: CODER
ACTION: RESPONSE
SUMMARY: Welcome to sirji-messages
BODY: Welcome to sirji-messages. Here's how you can start.
***"""

# Parsing the message
message = message_parse(message_str)
print(message)
````

### Allowed Response Templates

Provides the part of the system prompt describing allowed Response Templates for a given agent pair.

```python
from sirji_messages import allowed_response_templates, AgentEnum

# Generate allowed response templates
response_templates_str = allowed_response_templates(AgentEnum.ANY, AgentEnum.EXECUTOR)
print(response_templates_str)
```

### Handling Custom Exceptions

Efficiently manage parsing and validation errors with custom exceptions for improved error handling and debugging.

```python
from sirji_messages import MessageParsingError, MessageValidationError, message_parse

try:
    # Attempt parsing an incorrectly formatted message
    message_parse("INCORRECT_FORMAT")
except MessageParsingError as e:
    print(f"Parsing Error: {e}")
except MessageValidationError as e:
    print(f"Validation Error: {e}")
```

### Enums for Agents and Actions

Use enums (`ActionEnum`, `AgentEnum`) to reference actions and agent types programmatically, enhancing code clarity and reducing errors.

```python
from sirji_messages import ActionEnum, AgentEnum

# Example usage of enums for action and agent reference
action = ActionEnum.INVOKE_AGENT
agent = AgentEnum.ORCHESTRATOR

# Accessing enum properties
print(f"Action: {action.name}, Agent: {agent.full_name}")

# Access to enums using [] is also possible
action = ActionEnum['INVOKE_AGENT']
agent = AgentEnum['ORCHESTRATOR']
```

## For Contributors

1. Fork and clone the repository.
2. Create and activate the virtual environment as described above.
3. Install the package in editable mode by running the following command from repository root:

```zsh
pip install -e .
```

## Running Tests and Coverage Analysis

Follow the above mentioned steps for "contributors", before running the test cases.

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
