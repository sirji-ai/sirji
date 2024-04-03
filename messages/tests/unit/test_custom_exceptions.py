import pytest
from sirji_messages import MessageValidationError, MessageParsingError


def test_message_validation_error():
    with pytest.raises(MessageValidationError) as exc_info:
        raise MessageValidationError("Custom error message")
    assert str(
        exc_info.value) == "Custom error message", "MessageValidationError does not show the correct message"


def test_message_parsing_error():
    with pytest.raises(MessageParsingError) as exc_info:
        raise MessageParsingError("Parsing failed")
    assert str(
        exc_info.value) == "Parsing failed", "MessageParsingError does not show the correct message"
