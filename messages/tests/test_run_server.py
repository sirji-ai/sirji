import pytest
import textwrap
from sirji_messages.messages.actions.run_server import RunServerMessage

def test_run_server_message_sample():
    message = RunServerMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: EXECUTOR
    ACTION: RUN_SERVER
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    {{command}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_run_server_message_description():
    message = RunServerMessage()
    assert message.description() == "Run a Server or a Continuous Running Process"

def test_run_server_message_instructions():
    message = RunServerMessage()
    instructions = message.instructions()
    
    assert instructions == [
        "The command must use the project root as the current working directory.",
        "The command must be sufficiently chained. For example, 'source my_env.sh && npm start'."
    ]