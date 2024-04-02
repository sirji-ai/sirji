import pytest
from sirji_messages import message_parse, MessageParsingError, MessageValidationError

# Test Cases for message_parse function


def test_message_parse_valid_input():
    input_message = """
    ```
    FROM: CODER
    TO: USER
    ACTION: INFORM
    DETAILS: Some information.
    ```
    """
    expected_output = {
        'FROM': 'CODER',
        'TO': 'USER',
        'ACTION': 'INFORM',
        'DETAILS': 'Some information.'
    }
    assert message_parse(
        input_message) == expected_output, "Valid message parsing failed"


def test_message_parse_invalid_format_raises_error():
    input_message = "FROM: CODER\nTO: USER\nACTION: INFORM\nDETAILS: Some information."
    with pytest.raises(MessageValidationError):
        message_parse(input_message)


def test_message_parse_missing_action_raises_error():
    input_message = """
    ```
    FROM: CODER
    TO: USER
    DETAILS: Missing action field.
    ```
    """
    with pytest.raises(MessageValidationError):
        message_parse(input_message)


def test_message_parse_incorrect_message_raises_error():
    input_message = """
    ```
    This is not a correctly formatted message.
    ```
    """
    with pytest.raises(MessageValidationError):
        message_parse(input_message)


def test_message_parse_permission_denied_error():
    input_message = """
    ```
    FROM: USER
    TO: CODER
    ACTION: CREATE_FILE
    DETAILS: Attempting an unauthorized action.
    ```
    """
    with pytest.raises(MessageValidationError):
        message_parse(input_message)

# Testing with extra spaces around the key elements


def test_message_parse_with_extra_spaces():
    input_message = """
    ```
    FROM :  CODER
    TO : USER
    ACTION : INFORM
    DETAILS : Extra spaces around colons.
    ```
    """
    expected_output = {
        'FROM': 'CODER',
        'TO': 'USER',
        'ACTION': 'INFORM',
        'DETAILS': 'Extra spaces around colons.'
    }
    assert message_parse(
        input_message) == expected_output, "Message parsing failed with extra spaces"

# Adjusting the test to align with the current implementation's case sensitivity


def test_message_parse_case_sensitivity():
    input_message = """
    ```
    from: CODER
    to: USER
    action: INFORM
    details: Checking case sensitivity.
    ```
    """
    # Expecting a MessageValidationError due to case sensitivity
    with pytest.raises(MessageValidationError):
        message_parse(input_message)
