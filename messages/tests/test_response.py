import pytest
import textwrap
from sirji_messages.messages.actions.response import ResponseMessage

def test_response_message_sample():
    message = ResponseMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Agent Id of the agent sending the response}}
    TO: {{Your Agent ID}}
    ACTION: RESPONSE
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: Empty
    BODY: 
    {{Response}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_response_message_description():
    message = ResponseMessage()
    assert message.description() == "The response output"

def test_response_message_instructions():
    message = ResponseMessage()
    instructions = message.instructions()
    
    assert instructions == []