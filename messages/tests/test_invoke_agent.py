import pytest
import textwrap
from sirji_messages.messages.actions.invoke_agent import InvokeAgentMessage

def test_invoke_agent_message_sample():
    message = InvokeAgentMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: ORCHESTRATOR
    TO: {{To Agent ID}}
    ACTION: INVOKE_AGENT
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    {{Purpose of invocation}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_invoke_agent_message_description():
    message = InvokeAgentMessage()
    assert message.description() == "Invoke an agent in a fresh session"

def test_invoke_agent_message_instructions():
    message = InvokeAgentMessage()
    instructions = message.instructions()
    assert instructions == ["For first time invoking an agent, always use this action."]