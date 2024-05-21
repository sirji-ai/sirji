
import pytest
from sirji_messages import (
    message_parse,
    MessageFactory,
    ActionEnum,
    AgentEnum,
    MessageParsingError,
    MessageValidationError,
    validate_permission,
    permissions_dict,
    allowed_response_templates
)

def test_imports():
    # Test if all imports are available
    assert message_parse is not None
    assert MessageFactory is not None
    assert ActionEnum is not None
    assert AgentEnum is not None
    assert MessageParsingError is not None
    assert MessageValidationError is not None
    assert validate_permission is not None
    assert permissions_dict is not None
    assert allowed_response_templates is not None

def test_enum_members():
    # Test if enums have expected members
    assert ActionEnum.ANSWER.name == "ANSWER"
    assert AgentEnum.CODER.name == "CODER"

def test_exceptions():
    # Test if exceptions can be raised and caught
    with pytest.raises(MessageParsingError):
        raise MessageParsingError("Test parsing error")
    
    with pytest.raises(MessageValidationError):
        raise MessageValidationError("Test validation error")

def test_validate_permission():
    # Test if validate_permission function works as expected
    assert validate_permission("ANY", "EXECUTOR", "CREATE_PROJECT_FILE") == True
    assert validate_permission("ANY", "EXECUTOR", "INVALID_ACTION") == False

def test_allowed_response_templates():
    # Test if allowed_response_templates function works as expected
    from_agent = AgentEnum.ANY
    to_agent = AgentEnum.EXECUTOR
    action_list = permissions_dict[(from_agent, to_agent)]

    response_template = allowed_response_templates(from_agent, to_agent, action_list)
    
    assert "Allowed Response Templates TO EXECUTOR:" in response_template