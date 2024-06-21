
import pytest
import textwrap
from sirji_messages.messages.actions.train_using_url import TrainUsingUrlMessage

def test_train_using_url_message_sample():
    message = TrainUsingUrlMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: RESEARCHER
    ACTION: TRAIN_USING_URL
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    URL: {{url}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_train_using_url_message_description():
    message = TrainUsingUrlMessage()
    assert message.description() == "Train using a URL"

def test_train_using_url_message_instructions():
    message = TrainUsingUrlMessage()
    instructions = message.instructions()
    
    assert instructions == []