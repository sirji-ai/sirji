
import pytest
from sirji_messages.parser import parse, MessageParsingError, MessageValidationError

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
        'FROM': 'CODER',
        'TO': 'USER',
        'ACTION': 'INFORM',
        'STEP': 'step1',
        'SUMMARY': 'Welcome',
        'BODY': "Welcome to sirji-messages. Here's how you can start."
    }
    
    parsed_message = parse(message_str)
    assert parsed_message == expected_output

def test_parse_missing_property():
    message_str = """***
    FROM: CODER
    TO: USER
    ACTION: INFORM
    SUMMARY: Welcome
    ***"""
    
    with pytest.raises(MessageValidationError) as exc_info:
        parse(message_str)
    assert str(exc_info.value) == "Message does not meet the minimum length requirement"

def test_parse_invalid_action():
    message_str = """***
    FROM: CODER
    TO: USER
    ACTION: INVALID_ACTION
    STEP: step1
    SUMMARY: Welcome
    BODY: Welcome to sirji-messages. Here's how you can start.
    ***"""
    
    with pytest.raises(MessageValidationError) as exc_info:
        parse(message_str)
    assert str(exc_info.value) == "Action INVALID_ACTION is not recognized"

def test_parse_invalid_format():
    message_str = """**
    FROM: CODER
    TO: USER
    ACTION: INFORM
    STEP: step1
    SUMMARY: Welcome
    BODY: Welcome to sirji-messages. Here's how you can start.
    **"""
    
    with pytest.raises(MessageValidationError) as exc_info:
        parse(message_str)
    assert str(exc_info.value) == "Message must start and end with ***"

def test_parse_short_message():
    message_str = """***
    FROM: CODER
    TO: USER
    ACTION: INFORM
    ***"""
    
    with pytest.raises(MessageValidationError) as exc_info:
        parse(message_str)
    assert str(exc_info.value) == "Message does not meet the minimum length requirement"