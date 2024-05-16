import pytest
import textwrap
from sirji_messages.messages.actions.append_to_agent_output_index import AppendToAgentOutputIndexMessage

def test_append_to_agent_output_index_message_sample():
    message = AppendToAgentOutputIndexMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: EXECUTOR
    ACTION: APPEND_TO_AGENT_OUTPUT_INDEX
    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    File path: {{file path of the agent output file relative to the Agent Output Folder}}
    ---
    {{Description of the agent output file, to be used by other agents to know what it is about}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_append_to_agent_output_index_message_description():
    message = AppendToAgentOutputIndexMessage()
    assert message.description() == "Register to the Agent Output Index"

def test_append_to_agent_output_index_message_instructions():
    message = AppendToAgentOutputIndexMessage()
    instructions = message.instructions()
    
    assert instructions == [
        "Ensure to register new agent output files to the Agent Output Index.",
        "The file path must be in the following format: '{{Your Agent ID}}/{{file name}}'."
    ]