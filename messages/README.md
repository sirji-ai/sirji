# sirji-messages

`sirji-messages` is a Python package.

## Installation

Install `sirji-messages` quickly with pip:

```
pip install sirji-messages
```

## Usages

### Message Parser

The message parser can be used to parse the message string and return a dictionary with the following mandatory keys:

- `FROM`: The sender of the message.
- `TO`: The receiver of the message.
- `ACTION`: The action of the message.

````python
from sirji_messages import message_parse

message_str ="""```
FROM: CODER
TO: USER
ACTION: INFORM
DETAILS: Some information.
```"""

message = message_parse(message_str)
````

### Permissions

The permissions dictionary can be used to check if a particular action message is allowed between two agents.

```python
from sirji_messages import permissions_dict, validate_permission, AgentEnum

print(permissions_dict[(AgentEnum.CODER, AgentEnum.USER)])
print(validate_permission("CODER","USER", "QUESTION"))
```

### Custom Exceptions

The message parser can throw exceptions of following types:

- `MessageParsingError`: If the message string is not in the correct format.
- `MessageValidationError`: If the message string is in the correct format but the message is not valid.

````python
from sirji_messages import MessageParsingError, MessageValidationError, message_parse

input_message = """
`
FROM: CODER
TO: USER
ACTION: QUESTION
DETAILS: Test Question?```
"""

try:
    print(message_parse(input_message))
except Exception as e:
    if isinstance(e, MessageValidationError):
        print(e)
    elif isinstance(e, MessageParsingError):
        print(e)
````

### Action Enum

The action enum can be used to get the action message enum from the string. We can use either '.' or '[]' to get the enum.

```python
from sirji_messages import ActionEnum

# Access using '.'
action1 = ActionEnum.ACKNOWLEDGE

# Access using `[]`
action2 = ActionEnum['ACKNOWLEDGE']

# Get short name for the action
print(action1.name)
```

### Agent Enum

The agent enum can be used to get the agent enum from the string. We can use either '.' or '[]' to get the enum.

```python
from sirji_messages import AgentEnum

# Access using '.'
agent1 = AgentEnum.CODER

# Access using `[]`
agent2 = AgentEnum['CODER']

# Get short name for the agent
print(agent1.name)

# Get full name for the agent
print(agent1.full_name)
```

### Message Factory

The message factory can be used to get the message class from the action enum name.

```python
from sirji_messages import MessageFactory, ActionEnum
MessageClass = MessageFactory[ActionEnum.ACKNOWLEDGE.name]

# Get sample message
sample_message_str = MessageClass().sample()
print(sample_message_str)

# Generate message for specific template vars
generated_message_str = MessageClass().generate({})
print(generated_message_str)
```

### Agent System Prompt Factory

The agent system prompt factory can be used to get the system prompt class from the agent enum name.

```python
from sirji_messages import AgentSystemPromptFactory, AgentEnum
AgentSystemPromptClass = AgentSystemPromptFactory[AgentEnum.CODER.name]

# Get the system prompt for the agent
print(AgentSystemPromptClass().system_prompt())
```

## Running Tests and Coverage Analysis

Ensure you have `pytest` and `coverage.py` installed:

```zsh
pip install pytest coverage
```

In your project directory:

1. **Execute Tests:**

   ```zsh
   pytest
   ```

2. **Measure Coverage:**

   Exclude test files from the coverage report:

   ```zsh
   coverage run --omit="tests/*" -m pytest
   ```

   View the coverage report in the terminal:

   ```zsh
   coverage report
   ```

## License

`sirji-messages` is made available under the MIT License. See the included LICENSE file for more details.
