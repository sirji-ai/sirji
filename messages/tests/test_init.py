
import pytest
from sirji_messages import (
    message_parse,
    MessageFactory,
    ActionEnum,
    AgentEnum,
    MessageIncorrectFormatError,
    MessageMultipleActionError, 
    MessageUnRecognizedActionError, 
    MessageMissingPropertyError, 
    MessageLengthConstraintError,
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
    assert MessageIncorrectFormatError is not None
    assert MessageMissingPropertyError is not None
    assert MessageLengthConstraintError is not None
    assert MessageMultipleActionError is not None
    assert MessageUnRecognizedActionError is not None
    assert validate_permission is not None
    assert permissions_dict is not None
    assert allowed_response_templates is not None

def test_enum_members():
    # Test if enums have expected members
    assert ActionEnum.ANSWER.name == "ANSWER"
    assert AgentEnum.CODER.name == "CODER"

def test_exceptions():
    # Test if exceptions can be raised and caught
    with pytest.raises(MessageIncorrectFormatError) as exc_info:
        raise MessageIncorrectFormatError("Test incorrect format error")
    assert str(exc_info.value) == "Test incorrect format error"
    assert exc_info.value.message == "Test incorrect format error"

    with pytest.raises(MessageMultipleActionError) as exc_info:
        raise MessageMultipleActionError("Test multiple action error")
    assert str(exc_info.value) == "Test multiple action error"
    assert exc_info.value.message == "Test multiple action error"

    with pytest.raises(MessageUnRecognizedActionError) as exc_info:
        raise MessageUnRecognizedActionError("Test unrecognized action error")
    assert str(exc_info.value) == "Test unrecognized action error"
    assert exc_info.value.message == "Test unrecognized action error"

    with pytest.raises(MessageMissingPropertyError) as exc_info:
        raise MessageMissingPropertyError("Test missing property error")
    assert str(exc_info.value) == "Test missing property error"
    assert exc_info.value.message == "Test missing property error"

    with pytest.raises(MessageLengthConstraintError) as exc_info:
        raise MessageLengthConstraintError("Test length constraint error")
    assert str(exc_info.value) == "Test length constraint error"
    assert exc_info.value.message == "Test length constraint error"

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