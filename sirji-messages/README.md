# sirji-messages

`sirji-messages` is a Python package.

## Installation

Install `sirji-messages` quickly with pip:

```
pip install sirji-messages
```

## Usages

### Message Parser

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

### Custom Exceptions

```python
# message_parser can throw exceptions of following types.
from sirji_messages import MessageParsingError, MessageValidationError
```

### Action Enum

```python
from sirji_messages import ActionEnum

# We can use either '.' or '[]' to get the enum
action1 = ActionEnum.ACKNOWLEDGE
action2 = ActionEnum['ACKNOWLEDGE']
```

### Agent Enum

```python
from sirji_messages import AgentEnum

# We can use either '.' or '[]' to get the enum
agent1 = AgentEnum.CODER
agent2 = AgentEnum['CODER']
```

### Message Factory

```python
from sirji_messages import MessageFactory, ActionEnum
message_class = MessageFactory[ActionEnum.ACKNOWLEDGE.name]
```

## License

`sirji-messages` is made available under the MIT License. See the included LICENSE file for more details.
