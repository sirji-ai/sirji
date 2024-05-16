import pytest
from sirji_messages.custom_exceptions import MessageValidationError, MessageParsingError

def test_message_validation_error():
    with pytest.raises(MessageValidationError) as exc_info:
        raise MessageValidationError("Test validation error")
    assert str(exc_info.value) == "Test validation error"
    assert exc_info.value.message == "Test validation error"

def test_message_validation_error_default_message():
    with pytest.raises(MessageValidationError) as exc_info:
        raise MessageValidationError()
    assert str(exc_info.value) == "Invalid message format"
    assert exc_info.value.message == "Invalid message format"

def test_message_parsing_error():
    with pytest.raises(MessageParsingError) as exc_info:
        raise MessageParsingError("Test parsing error")
    assert str(exc_info.value) == "Test parsing error"
    assert exc_info.value.message == "Test parsing error"

def test_message_parsing_error_default_message():
    with pytest.raises(MessageParsingError) as exc_info:
        raise MessageParsingError()
    assert str(exc_info.value) == "Error parsing message"
    assert exc_info.value.message == "Error parsing message"