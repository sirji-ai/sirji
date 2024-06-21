import pytest
import textwrap
from sirji_messages.messages.actions.create_project_file import CreateProjectFileMessage

def test_create_project_file_message_sample():
    message = CreateProjectFileMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: EXECUTOR
    ACTION: CREATE_PROJECT_FILE
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    File path: {{file path}}
    ---
    {{file contents}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_create_project_file_message_description():
    message = CreateProjectFileMessage()
    assert message.description() == "Create a File Inside Project Folder Only"

def test_create_project_file_message_instructions():
    message = CreateProjectFileMessage()
    instructions = message.instructions()
    
    assert instructions == [
        "The file path must be relative to the project root.",
        "The file contents should never be enclosed within ``` starting and ending markers."
    ]