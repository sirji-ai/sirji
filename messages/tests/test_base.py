
import pytest
import textwrap
from sirji_messages.messages.actions.base import BaseMessages

class TestMessage(BaseMessages):
    def __init__(self):
        self.action = "TEST_ACTION"

    def sample(self):
        return "Sample message"

    def description(self):
        return "Test message description"

    def instructions(self):
        return ["Instruction 1", "Instruction 2"]

def test_base_message_abstract_methods():
    test_message = TestMessage()
    
    assert test_message.sample() == "Sample message"
    assert test_message.description() == "Test message description"
    assert test_message.instructions() == ["Instruction 1", "Instruction 2"]

def test_base_message_generate():
    test_message = TestMessage()
    obj = {
        "from_agent_id": "AGENT_1",
        "to_agent_id": "AGENT_2",
        "step": "Provide the step number here for the ongoing step if any.",
        "summary": "Test summary",
        "body": "Test body",
    }
    expected_output = textwrap.dedent("""
    ***
    FROM: AGENT_1
    TO: AGENT_2
    ACTION: TEST_ACTION
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: Test summary
    BODY: Test body
    ***""")
    
    generated_message = test_message.generate(obj).strip()
    assert generated_message == expected_output.strip()

def test_base_message_generate_with_missing_keys():
    test_message = TestMessage()
    obj = {
        "from_agent_id": "AGENT_1",
        "summary": "Test summary",
        "body": "Test body"
    }
    with pytest.raises(KeyError):
        test_message.generate(obj)