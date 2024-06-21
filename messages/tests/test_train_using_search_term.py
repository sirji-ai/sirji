
import pytest
import textwrap
from sirji_messages.messages.actions.train_using_search_term import TrainUsingSearchTermMessage

def test_train_using_search_term_message_sample():
    message = TrainUsingSearchTermMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: RESEARCHER
    ACTION: TRAIN_USING_SEARCH_TERM
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    Term: {{search term}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_train_using_search_term_message_description():
    message = TrainUsingSearchTermMessage()
    assert message.description() == "Train using a search term"

def test_train_using_search_term_message_instructions():
    message = TrainUsingSearchTermMessage()
    instructions = message.instructions()
    
    assert instructions == []