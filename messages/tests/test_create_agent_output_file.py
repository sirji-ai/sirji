
import pytest
import textwrap
from sirji_messages.messages.actions.create_agent_output_file import CreateAgentOutputFileMessage

def test_create_agent_output_file_message_sample():
    message = CreateAgentOutputFileMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: EXECUTOR
    ACTION: CREATE_AGENT_OUTPUT_FILE
    SUMMARY: {{{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    File path: {{file path}}
    ---
    {{file contents}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_create_agent_output_file_message_description():
    message = CreateAgentOutputFileMessage()
    assert message.description() == "Create a File Inside Agent Output Folder"

def test_create_agent_output_file_message_instructions():
    message = CreateAgentOutputFileMessage()
    instructions = message.instructions()
    
    assert instructions == [
        "The file path must be in the following format: '{{Your Agent ID}}/{{file name}}'."
    ]