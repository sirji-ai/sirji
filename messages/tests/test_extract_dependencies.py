
import pytest
import textwrap
from sirji_messages.messages.actions.extract_dependencies import ExtractDependenciesMessage

def test_extract_dependencies_message_sample():
    message = ExtractDependenciesMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: EXECUTOR
    ACTION: EXTRACT_DEPENDENCIES
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    {{Array of file paths}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_extract_dependencies_message_description():
    message = ExtractDependenciesMessage()
    assert message.description() == "Extract Dependencies of The Specified Files"

def test_extract_dependencies_message_instructions():
    message = ExtractDependenciesMessage()
    instructions = message.instructions()
    
    assert instructions == ["The file path must be relative to the project root."]