import pytest
from sirji_messages.helper import allowed_response_templates
from sirji_messages.agent_enum import AgentEnum
from sirji_messages.permissions import permissions_dict

def test_allowed_response_templates():
    from_agent = AgentEnum.ANY
    to_agent = AgentEnum.EXECUTOR
    response_template = allowed_response_templates(from_agent, to_agent)
    
    assert "Allowed Response Templates TO EXECUTOR:" in response_template
    assert "Function 1. " in response_template
    assert "Response template:" in response_template

def test_allowed_response_templates_orchestrator_to_any():
    from_agent = AgentEnum.ORCHESTRATOR
    to_agent = AgentEnum.ANY
    response_template = allowed_response_templates(from_agent, to_agent)
    
    assert "To invoke an agent, please respond with the text below" in response_template
    assert "Function 1. " in response_template
    assert "Response template:" in response_template

def test_allowed_response_templates_any_to_caller():
    from_agent = AgentEnum.ANY
    to_agent = AgentEnum.CALLER
    response_template = allowed_response_templates(from_agent, to_agent)
    
    assert "Respond to the agent which invoked you" in response_template
    assert "Function 1. " in response_template
    assert "Response template:" in response_template

def test_allowed_response_templates_invalid_agents():
    from_agent = 'INVALID_AGENT'
    to_agent = AgentEnum.EXECUTOR
    with pytest.raises(KeyError):
        allowed_response_templates(from_agent, to_agent)