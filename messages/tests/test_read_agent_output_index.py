import pytest
import textwrap
from sirji_messages.messages.actions.read_agent_output_index import ReadAgentOutputIndexMessage

def test_read_agent_output_index_message_sample():
    message = ReadAgentOutputIndexMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: EXECUTOR
    ACTION: READ_AGENT_OUTPUT_INDEX
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    Empty
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_read_agent_output_index_message_description():
    message = ReadAgentOutputIndexMessage()
    assert message.description() == "Read Agent Output Index"

def test_read_agent_output_index_message_instructions():
    message = ReadAgentOutputIndexMessage()
    instructions = message.instructions()
    
    assert instructions == []