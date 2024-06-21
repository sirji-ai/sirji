import pytest
import textwrap
from sirji_messages.messages.actions.search_code_in_project import SearchCodeInProject

def test_search_code_in_project_message_sample():
    message = SearchCodeInProject()
    sample_message = message.sample()

    print(sample_message)
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: EXECUTOR
    ACTION: SEARCH_CODE_IN_PROJECT
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    Search Term: {{Search term}}
    ---
    ***
    """)

    print(expected_output)
    
    assert sample_message.strip() == expected_output.strip()

def test_search_code_in_project_message_description():
    message = SearchCodeInProject()
    assert message.description() == "Search for code in a directory and all its subdirectories"

def test_search_code_in_project_message_instructions():
    message = SearchCodeInProject()
    instructions = message.instructions()
    
    assert instructions == []

