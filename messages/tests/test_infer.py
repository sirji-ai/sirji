
import pytest
import textwrap
from sirji_messages.messages.actions.infer import InferMessage

def test_infer_message_sample():
    message = InferMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: RESEARCHER
    ACTION: INFER
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    {{query}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_infer_message_description():
    message = InferMessage()
    assert message.description() == "Ask questions on the trained content"

def test_infer_message_instructions():
    message = InferMessage()
    instructions = message.instructions()
    
    assert instructions == []