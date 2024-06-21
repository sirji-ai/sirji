import pytest
import textwrap
from sirji_messages.messages.actions.invoke_agent_existing_session import InvokeAgentExistingSessionMessage

def test_invoke_agent_existing_session_message_sample():
    message = InvokeAgentExistingSessionMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: ORCHESTRATOR
    TO: {{To Agent ID}}
    ACTION: INVOKE_AGENT_EXISTING_SESSION
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    {{Purpose of invocation}}
    ***""")

    print(f"Expected Output: {expected_output}")

    print(f"Sample Message: {sample_message}")
    
    assert sample_message.strip() == expected_output.strip()

def test_invoke_agent_existing_session_message_description():
    message = InvokeAgentExistingSessionMessage()
    assert message.description() == "Invoke an agent continuing on the existing session"

def test_invoke_agent_existing_session_message_instructions():
    message = InvokeAgentExistingSessionMessage()
    instructions = message.instructions()
    
    assert instructions == ["Never use this action while invoking an agent for the first time."]