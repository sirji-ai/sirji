
import pytest
import textwrap
from sirji_messages.messages.actions.question import QuestionMessage

def test_question_message_sample():
    message = QuestionMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: SIRJI_USER
    ACTION: QUESTION
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: Empty
    BODY: 
    {{Question}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_question_message_description():
    message = QuestionMessage()
    assert message.description() == "Ask a question"

def test_question_message_instructions():
    message = QuestionMessage()
    instructions = message.instructions()
    
    assert instructions == []