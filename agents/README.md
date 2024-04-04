# sirji-agents

`sirji-agents` is a PyPI package that implements three key agents for Sirji:

- Coding Agent
- Planning Agent
- Research Agent

It Utilizes:

- OpenAI Chat Completions API
- OpenAI Assistants API

This package communicates with models and RAG assistants.

## Installation

```zsh
pip install sirji-agents
```

Run the following to enable playwright:

```zsh
playwright install
```

## Usages

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

## License

Distributed under the MIT License. See `LICENSE` for more information.
