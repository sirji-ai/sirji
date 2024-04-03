import pytest
from sirji_messages.system_prompts.agents.base import AgentSystemPromptBase
from sirji_messages.system_prompts.factory import AgentSystemPromptFactory
from sirji_messages import AgentEnum


@pytest.mark.parametrize("agent_class", [
    AgentSystemPromptFactory[AgentEnum.CODER.name],
    AgentSystemPromptFactory[AgentEnum.PLANNER.name],
    # Add all agent classes
])
def test_agent_system_prompt_base_integration(agent_class):
    agent_instance = agent_class()
    prompt_text = agent_instance.system_prompt()

    assert isinstance(prompt_text, str), "System prompt text must be a string"
    assert len(prompt_text) > 0, "System prompt text should not be empty"
    # This can be expanded with specific checks for each agent type

# Additionally, test other methods and properties if applicable
