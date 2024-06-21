import pytest
import textwrap
from sirji_messages.messages.actions.read_agent_output_files import ReadAgentOutputFilesMessage

def test_read_agent_output_files_message_sample():
    message = ReadAgentOutputFilesMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: EXECUTOR
    ACTION: READ_AGENT_OUTPUT_FILES
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    File paths: {{Array of file paths}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_read_agent_output_files_message_description():
    message = ReadAgentOutputFilesMessage()
    assert message.description() == "Read Multiple Files From Agent Output Folder"

def test_read_agent_output_files_message_instructions():
    message = ReadAgentOutputFilesMessage()
    instructions = message.instructions()
    assert instructions == ["The body must be in the following format: File paths: [\{{Your_agent_id}}/{{file_name}}\]"]