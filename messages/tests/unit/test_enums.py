import pytest
from sirji_messages import AgentEnum, ActionEnum

# Test Cases for AgentEnum


def test_agent_enum_values_and_full_names():
    assert AgentEnum.CODER.value == 1, "CODER value mismatch"
    assert AgentEnum.CODER.full_name == "Coding Agent", "CODER full name mismatch"
    assert AgentEnum.USER.value == 5, "USER value mismatch"
    assert AgentEnum.USER.full_name == "End User", "USER full name mismatch"


def test_agent_enum_names():
    assert AgentEnum.CODER.name == "CODER", "Incorrect name for CODER"
    assert AgentEnum.USER.name == "USER", "Incorrect name for USER"

# Test Cases for ActionEnum


def test_action_enum_auto_values():
    # Test specific actions to ensure their auto-generated values are distinct
    assert ActionEnum.ACKNOWLEDGE.value != ActionEnum.ANSWER.value, "ACKNOWLEDGE and ANSWER values should not be equal"
    assert ActionEnum.EXECUTE_COMMAND.value != ActionEnum.CREATE_FILE.value, "EXECUTE_COMMAND and CREATE_FILE values should not be equal"


def test_action_enum_membership():
    # Check if certain actions are in the ActionEnum
    assert "INFORM" in ActionEnum.__members__, "INFORM should be a member of ActionEnum"
    assert "QUESTION" in ActionEnum.__members__, "QUESTION should be a member of ActionEnum"
