# sirji-messages

`sirji-messages` is a PyPI package that implements the Sirji message protocol with following highlights:

- Message Factory
- Permissions Matrix (for defining message actions allowed between two agents)
- System prompt generation

## Installation

```bash
pip install sirji-messages
```

## Features and Usage

### Message Parsing

Parse structured message strings into Python dictionaries for easy access to the message components.

```python
from sirji_messages import message_parse

# Example message string to parse
message_str = """```
FROM: CODER
TO: USER
ACTION: INFORM
DETAILS: Welcome to sirji-messages. Here's how you can start.
```"""

# Parsing the message
message = message_parse(message_str)
print(message)
```

### Permission Validation

Determine if a specified action is allowed between two agents based on predefined permission rules.

```python
from sirji_messages import permissions_dict, validate_permission, AgentEnum

# Example check if a CODER can QUESTION a USER
is_allowed = validate_permission("CODER", "USER", "QUESTION")
print(f"Is allowed: {is_allowed}")

# Get a direct look at permissions dictionary for CODER sending to USER
print(permissions_dict[(AgentEnum.CODER, AgentEnum.USER)])
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

### Enums for Intuitive References

Use enums (`ActionEnum`, `AgentEnum`) to reference actions and agent types programmatically, enhancing code clarity and reducing errors.

```python
from sirji_messages import ActionEnum, AgentEnum

# Example usage of enums for action and agent reference
action = ActionEnum.ACKNOWLEDGE
agent = AgentEnum.CODER

# Accessing enum properties
print(f"Action: {action.name}, Agent: {agent.full_name}")

# Access to enums using [] is also possible
action = ActionEnum['ACKNOWLEDGE']
agent = AgentEnum['CODER']
```

### Factories for Dynamic Message and Prompt Creation

Utilize factories (`MessageFactory`, `AgentSystemPromptFactory`) to instantiate message and prompt classes dynamically based on enums. It simplifies creating custom messages or retrieving specific system prompts without hardcoding class names.

```python
from sirji_messages import MessageFactory, ActionEnum, AgentSystemPromptFactory, AgentEnum

# Message class instantiation from an action enum
message_class = MessageFactory[ActionEnum.INFORM.name]
print(f"Sample INFORM message:\n{message_class().sample()}")

# Generate message using passed template variables
generated_messages = message_class().generate({"details": "Some sample information."})
print(f"Generated INFORM message:\n{generated_messages}")

# System prompt class instantiation from an agent enum
prompt_class = AgentSystemPromptFactory[AgentEnum.CODER.name]
print(f"CODER system prompt: {prompt_class().system_prompt()}")
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
