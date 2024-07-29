import pytest
from sirji_messages.parser import parse
from sirji_messages.custom_exceptions import (
    MessageIncorrectFormatError,
    MessageMultipleActionError,
    MessageLengthConstraintError,
)
from sirji_messages.action_enum import ActionEnum


def test_parse_valid_message():
    message_str = """***
    FROM: CODER
    TO: USER
    ACTION: INFORM
    STEP: step1
    SUMMARY: Welcome
    BODY: Welcome to sirji-messages. Here's how you can start.
    ***"""

    expected_output = {
        "FROM": "CODER",
        "TO": "USER",
        "ACTION": "INFORM",
        "STEP": "step1",
        "SUMMARY": "Welcome",
        "BODY": "Welcome to sirji-messages. Here's how you can start.",
    }

    parsed_message = parse(message_str)
    assert parsed_message == expected_output


def test_parse_invalid_format():
    message_str = """**
    FROM: CODER
    TO: USER
    ACTION: INFORM
    STEP: step1
    SUMMARY: Welcome
    BODY: Welcome to sirji-messages. Here's how you can start.
    **"""

    with pytest.raises(MessageIncorrectFormatError) as exc_info:
        parse(message_str)
    assert "Message must start and end with ***" in str(exc_info.value)


def test_parse_short_message():
    message_str = """***
    FROM: CODER
    TO: USER
    ACTION: INFORM
    ***"""

    with pytest.raises(MessageLengthConstraintError) as exc_info:
        parse(message_str)
    assert "Message does not meet the minimum length requirement" in str(exc_info.value)


def test_parse_multiple_action():
    message_str = """***
    FROM: CODER
    TO: USER
    ACTION: INFORM
    ACTION: ACTION_TOO_MANY
    STEP: step1
    SUMMARY: Welcome
    BODY: Welcome to sirji-messages. Here's how you can start.
    ***"""

    with pytest.raises(MessageMultipleActionError) as exc_info:
        parse(message_str)
    assert "Message contains more than one ACTION keyword" in str(exc_info.value)


# Remaining test cases

def test_parse_message_with_minimal_body():
    message_str = """***
    FROM: CODER
    TO: USER
    ACTION: INFORM
    STEP: step1
    SUMMARY: Welcome
    BODY: Welcome.
    ***"""

    expected_output = {
        "FROM": "CODER",
        "TO": "USER",
        "ACTION": "INFORM",
        "STEP": "step1",
        "SUMMARY": "Welcome",
        "BODY": "Welcome.",
    }

    parsed_message = parse(message_str)

    for key in expected_output:
        assert parsed_message[key].strip() == expected_output[key].strip()


def test_parse_message_with_empty_body():
    message_str = """***
    FROM: CODER
    TO: USER
    ACTION: INFORM
    STEP: step1
    SUMMARY: Welcome
    BODY:
    ***"""

    expected_output = {
        "FROM": "CODER",
        "TO": "USER",
        "ACTION": "INFORM",
        "STEP": "step1",
        "SUMMARY": "Welcome",
        "BODY": "",
    }

    parsed_message = parse(message_str)

    for key in expected_output:
        assert parsed_message[key].strip() == expected_output[key].strip()


def test_parse_message_with_whitespace():
    message_str = """   ***
    FROM:    CODER   
    TO: USER 
    ACTION:     INFORM
    STEP: step1    
    SUMMARY: Welcome   
    BODY:      

    Welcome to sirji-messages. Here's how you can start.
    ***
    """

    expected_output = {
        "FROM": "CODER",
        "TO": "USER",
        "ACTION": "INFORM",
        "STEP": "step1",
        "SUMMARY": "Welcome",
        "BODY": "Welcome to sirji-messages. Here's how you can start.",
    }

    parsed_message = parse(message_str)

    for key in expected_output:
        assert parsed_message[key].strip() == expected_output[key].strip()