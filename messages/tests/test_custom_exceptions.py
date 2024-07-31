import pytest
from sirji_messages.custom_exceptions import MessageIncorrectFormatError, MessageMultipleActionError, MessageUnRecognizedActionError, MessageMissingPropertyError, MessageLengthConstraintError


def test_message_incorrect_format_error():
    with pytest.raises(MessageIncorrectFormatError) as exc_info:
        raise MessageIncorrectFormatError("Test incorrect format error")
    assert str(exc_info.value) == "Test incorrect format error"
    assert exc_info.value.message == "Test incorrect format error"

def test_message_incorrect_format_error_default_message():
    with pytest.raises(MessageIncorrectFormatError) as exc_info:
        raise MessageIncorrectFormatError()
    assert str(exc_info.value) == "Message must start and end with ***"
    assert exc_info.value.message == "Message must start and end with ***"

def test_message_multiple_action_error():
    with pytest.raises(MessageMultipleActionError) as exc_info:
        raise MessageMultipleActionError("Test multiple action error")
    assert str(exc_info.value) == "Test multiple action error"
    assert exc_info.value.message == "Test multiple action error"

def test_message_multiple_action_error_default_message():
    with pytest.raises(MessageMultipleActionError) as exc_info:
        raise MessageMultipleActionError()
    assert str(exc_info.value) == "Message contains more than one ACTION keyword"
    assert exc_info.value.message == "Message contains more than one ACTION keyword"

def test_message_unrecognized_action_error():
    with pytest.raises(MessageUnRecognizedActionError) as exc_info:
        raise MessageUnRecognizedActionError("Test unrecognized action error")
    assert str(exc_info.value) == "Test unrecognized action error"
    assert exc_info.value.message == "Test unrecognized action error"

def test_message_unrecognized_action_error_default_message():
    with pytest.raises(MessageUnRecognizedActionError) as exc_info:
        raise MessageUnRecognizedActionError()
    assert str(exc_info.value) == "Action is not recognized"
    assert exc_info.value.message == "Action is not recognized"

def test_message_missing_property_error():
    with pytest.raises(MessageMissingPropertyError) as exc_info:
        raise MessageMissingPropertyError("Test missing property error")
    assert str(exc_info.value) == "Test missing property error"
    assert exc_info.value.message == "Test missing property error"

def test_message_missing_property_error_default_message():
    with pytest.raises(MessageMissingPropertyError) as exc_info:
        raise MessageMissingPropertyError()
    assert str(exc_info.value) == "Message does not contain required property"
    assert exc_info.value.message == "Message does not contain required property"

def test_message_length_constraint_error():
    with pytest.raises(MessageLengthConstraintError) as exc_info:
        raise MessageLengthConstraintError("Test length constraint error")
    assert str(exc_info.value) == "Test length constraint error"
    assert exc_info.value.message == "Test length constraint error"

def test_message_length_constraint_error_default_message():
    with pytest.raises(MessageLengthConstraintError) as exc_info:
        raise MessageLengthConstraintError()
    assert str(exc_info.value) == "Message does not meet the minimum length requirement"
    assert exc_info.value.message == "Message does not meet the minimum length requirement"