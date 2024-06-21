import pytest
import textwrap
from sirji_messages.messages.actions.store_in_scratch_pad import StoreInScratchPad

def test_store_in_scratch_pad_message_sample():
    message = StoreInScratchPad()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: EXECUTOR
    ACTION: STORE_IN_SCRATCH_PAD
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: {{notes}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_store_in_scratch_pad_message_description():
    message = StoreInScratchPad()
    assert message.description() == "Store Notes in the scratchpad"

def test_store_in_scratch_pad_message_instructions():
    message = StoreInScratchPad()
    instructions = message.instructions()
    
    assert instructions == [ "The command is used to store notes in the scratchpad.",]

