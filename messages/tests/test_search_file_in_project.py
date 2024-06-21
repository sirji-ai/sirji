
import pytest
import textwrap
from sirji_messages.messages.actions.search_file_in_project import SearchFileInProject

def test_search_file_in_project_message_sample():
    message = SearchFileInProject()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: EXECUTOR
    ACTION: SEARCH_FILE_IN_PROJECT
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    Search: {{Search term}}
    ---
    Directory: {{Directory path}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_search_file_in_project_message_description():
    message = SearchFileInProject()
    assert message.description() == "Search for a file in a directory and all its subdirectories"

def test_search_file_in_project_message_instructions():
    message = SearchFileInProject()
    instructions = message.instructions()
    
    assert instructions == []