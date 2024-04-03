import pytest
from sirji_messages import validate_permission, AgentEnum, ActionEnum

# Test cases for validate_permission function


def test_permission_valid():
    # Assuming Coder has permission to inform a User
    assert validate_permission(
        "CODER", "USER", "INFORM"), "Valid permission was denied"


def test_permission_invalid_action():
    # Assuming Coder does not have permission to execute a command directly to a User
    assert not validate_permission(
        "CODER", "USER", "EXECUTE_COMMAND"), "Invalid action was erroneously permitted"


def test_permission_invalid_agent_pair():
    # Assuming no direct interaction is allowed from Executor to User
    assert not validate_permission(
        "EXECUTOR", "USER", "INFORM"), "Invalid agent pair was erroneously permitted"


def test_permission_nonexistent_from_agent():
    assert not validate_permission(
        "FAKE_AGENT", "USER", "INFORM"), "Permission check with nonexistent 'from' agent should be denied"


def test_permission_nonexistent_to_agent():
    assert not validate_permission(
        "CODER", "FAKE_AGENT", "INFORM"), "Permission check with nonexistent 'to' agent should be denied"


def test_permission_nonexistent_action():
    assert not validate_permission(
        "CODER", "USER", "FAKE_ACTION"), "Permission check with nonexistent action should be denied"

# Testing with invalid agent enums


def test_permission_with_invalid_agent_enum():
    assert not validate_permission(
        "INVALID_AGENT", "USER", "INFORM"), "Permission check with invalid enum should return False instead of raising KeyError"
