
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
    generate_allowed_response_template
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
    assert generate_allowed_response_template is not None

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

def test_generate_allowed_response_template():
    # Test if generate_allowed_response_template function works as expected
    from_agent = AgentEnum.ANY
    to_agent = AgentEnum.EXECUTOR
    response_template = generate_allowed_response_template(from_agent, to_agent)
    
    assert "Allowed Response Templates TO EXECUTOR:" in response_template