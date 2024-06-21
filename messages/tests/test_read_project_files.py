
import pytest
import textwrap
from sirji_messages.messages.actions.read_project_files import ReadProjectFilesMessage

def test_read_project_files_message_sample():
    message = ReadProjectFilesMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: EXECUTOR
    ACTION: READ_PROJECT_FILES
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    File paths: {{Array of file paths}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_read_project_files_message_description():
    message = ReadProjectFilesMessage()
    assert message.description() == "Read Multiple Files From Project Folder Only"

def test_read_project_files_message_instructions():
    message = ReadProjectFilesMessage()
    instructions = message.instructions()
    
    assert instructions == ["The file paths must be relative to the project root."]