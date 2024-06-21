import pytest
import textwrap
from sirji_messages.messages.actions.execute_command import ExecuteCommandMessage

def test_execute_command_message_sample():
    message = ExecuteCommandMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: EXECUTOR
    ACTION: EXECUTE_COMMAND
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    {{command}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_execute_command_message_description():
    message = ExecuteCommandMessage()
    assert message.description() == "Execute a Command, Install Packages, or Install Dependencies"

def test_execute_command_message_instructions():
    message = ExecuteCommandMessage()
    instructions = message.instructions()
    
    assert instructions == [
        "The command must use the project root as the current working directory.",
        "The command must be sufficiently chained. For example, 'source venv/bin/activate && pip install openai', 'cd server && npm run start'."
    ]