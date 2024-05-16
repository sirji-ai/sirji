import pytest
from sirji_messages.permissions import validate_permission, permissions_dict
from sirji_messages.agent_enum import AgentEnum
from sirji_messages.action_enum import ActionEnum

def test_validate_permission_valid():
    assert validate_permission("ANY", "EXECUTOR", "CREATE_PROJECT_FILE") == True
    assert validate_permission("ANY", "SIRJI_USER", "QUESTION") == True
    assert validate_permission("ORCHESTRATOR", "SIRJI_USER", "SOLUTION_COMPLETE") == True
    assert validate_permission("ORCHESTRATOR", "ANY", "INVOKE_AGENT") == True

def test_validate_permission_invalid():
    assert validate_permission("ANY", "EXECUTOR", "INVALID_ACTION") == False
    assert validate_permission("ANY", "INVALID_AGENT", "QUESTION") == False
    assert validate_permission("INVALID_AGENT", "SIRJI_USER", "QUESTION") == False
    assert validate_permission("ORCHESTRATOR", "SIRJI_USER", "INVALID_ACTION") == False

def test_permissions_dict():
    assert (AgentEnum.ANY, AgentEnum.EXECUTOR) in permissions_dict
    assert ActionEnum.CREATE_PROJECT_FILE in permissions_dict[(AgentEnum.ANY, AgentEnum.EXECUTOR)]
    assert ActionEnum.QUESTION in permissions_dict[(AgentEnum.ANY, AgentEnum.SIRJI_USER)]
    assert ActionEnum.SOLUTION_COMPLETE in permissions_dict[(AgentEnum.ORCHESTRATOR, AgentEnum.SIRJI_USER)]
    assert ActionEnum.INVOKE_AGENT in permissions_dict[(AgentEnum.ORCHESTRATOR, AgentEnum.ANY)]

def test_permissions_dict_invalid():
    assert ('INVALID_AGENT', AgentEnum.EXECUTOR) not in permissions_dict
    assert 'INVALID_ACTION' not in permissions_dict[(AgentEnum.ANY, AgentEnum.EXECUTOR)]
    assert 'INVALID_ACTION' not in permissions_dict[(AgentEnum.ANY, AgentEnum.SIRJI_USER)]
    assert 'INVALID_ACTION' not in permissions_dict[(AgentEnum.ORCHESTRATOR, AgentEnum.SIRJI_USER)]
    assert 'INVALID_ACTION' not in permissions_dict[(AgentEnum.ORCHESTRATOR, AgentEnum.ANY)]