import pytest
import textwrap
from sirji_messages.messages.actions.store_in_agent_output import StoreInAgentOutputMessage

def test_store_in_agent_output_message_sample():
    message = StoreInAgentOutputMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: EXECUTOR
    ACTION: STORE_IN_AGENT_OUTPUT
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    File path: {{file path}}
    ---
    File content: {{file contents}}                     
    ---
    File content description: {{Description of the agent output file, to be used by other agents to know what it is about}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_store_in_agent_output_message_description():
    message = StoreInAgentOutputMessage()
    assert message.description() == "Create a file in the Agent Output Folder and register it to the Agent Output Index file"

def test_store_in_agent_output_message_instructions():
    message = StoreInAgentOutputMessage()
    instructions = message.instructions()
    
    assert instructions == [
        "The file path must be in the following format: '{{Your Agent ID}}/{{file name}}'."
    ]