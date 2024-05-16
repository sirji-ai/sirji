
import pytest
from sirji_messages.agent_enum import AgentEnum

def test_agent_enum_values():
    assert AgentEnum.ORCHESTRATOR.value == 0
    assert AgentEnum.CODER.value == 1
    assert AgentEnum.PLANNER.value == 2
    assert AgentEnum.EXECUTOR.value == 3
    assert AgentEnum.RESEARCHER.value == 4
    assert AgentEnum.SIRJI_USER.value == 5
    assert AgentEnum.ANY.value == 6
    assert AgentEnum.CALLER.value == 7

def test_agent_enum_full_names():
    assert AgentEnum.ORCHESTRATOR.full_name == "Orchestrator"
    assert AgentEnum.CODER.full_name == "Coding Agent"
    assert AgentEnum.PLANNER.full_name == "Planning Agent"
    assert AgentEnum.EXECUTOR.full_name == "Execution Agent"
    assert AgentEnum.RESEARCHER.full_name == "Research Agent"
    assert AgentEnum.SIRJI_USER.full_name == "End User"
    assert AgentEnum.ANY.full_name == "Any Agent"
    assert AgentEnum.CALLER.full_name == "Caller Agent"

def test_agent_enum_membership():
    assert AgentEnum['ORCHESTRATOR'] == AgentEnum.ORCHESTRATOR
    assert AgentEnum['CODER'] == AgentEnum.CODER
    assert AgentEnum['PLANNER'] == AgentEnum.PLANNER
    assert AgentEnum['EXECUTOR'] == AgentEnum.EXECUTOR
    assert AgentEnum['RESEARCHER'] == AgentEnum.RESEARCHER
    assert AgentEnum['SIRJI_USER'] == AgentEnum.SIRJI_USER
    assert AgentEnum['ANY'] == AgentEnum.ANY
    assert AgentEnum['CALLER'] == AgentEnum.CALLER
