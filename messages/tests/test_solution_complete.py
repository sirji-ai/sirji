
import pytest
import textwrap
from sirji_messages.messages.actions.solution_complete import SolutionCompleteMessage

def test_solution_complete_message_sample():
    message = SolutionCompleteMessage()
    sample_message = message.sample()
    
    expected_output = textwrap.dedent("""
    ***
    FROM: {{Your Agent ID}}
    TO: SIRJI_USER
    ACTION: SOLUTION_COMPLETE
    STEP: "Provide the step number here for the ongoing step if any."
    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
    BODY: 
    {{Summarize what all was done for getting the solution.}}
    ***""")
    
    assert sample_message.strip() == expected_output.strip()

def test_solution_complete_message_description():
    message = SolutionCompleteMessage()
    assert message.description() == "Inform About Solution Completed"

def test_solution_complete_message_instructions():
    message = SolutionCompleteMessage()
    instructions = message.instructions()
    
    assert instructions == []