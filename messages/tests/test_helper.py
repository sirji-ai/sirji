import pytest
from sirji_messages.helper import allowed_response_templates
from sirji_messages.agent_enum import AgentEnum
from sirji_messages.permissions import permissions_dict

def test_allowed_response_templates():
    from_agent = AgentEnum.ANY
    to_agent = AgentEnum.EXECUTOR
    action_list = permissions_dict[(from_agent, to_agent)]
    print("action_list", action_list)
    response_template = allowed_response_templates(from_agent, to_agent, action_list)
    
    assert "Allowed Response Templates TO EXECUTOR:" in response_template
    assert "Function 1. " in response_template
    assert "Response template:" in response_template

def test_allowed_response_templates_orchestrator_to_any():
    from_agent = AgentEnum.ORCHESTRATOR
    to_agent = AgentEnum.ANY
    action_list = permissions_dict[(from_agent, to_agent)]
    response_template = allowed_response_templates(from_agent, to_agent, action_list)
    
    assert "To invoke an agent, please respond with the text below" in response_template
    assert "Function 1. " in response_template
    assert "Response template:" in response_template

def test_allowed_response_templates_any_to_caller():
    from_agent = AgentEnum.ANY
    to_agent = AgentEnum.CALLER
    action_list = permissions_dict[(from_agent, to_agent)]
    response_template = allowed_response_templates(from_agent, to_agent, action_list)
    
    assert "Respond to the agent which invoked you" in response_template
    assert "Function 1. " in response_template
    assert "Response template:" in response_template

def test_allowed_response_templates_invalid_agents():
    from_agent = 'INVALID_AGENT'
    to_agent = AgentEnum.EXECUTOR
    with pytest.raises(KeyError):
        action_list = permissions_dict[(from_agent, to_agent)]
        allowed_response_templates(from_agent, to_agent, action_list)