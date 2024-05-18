import pytest
from sirji_messages import ActionEnum
def test_action_enum_membership():
    assert ActionEnum['ANSWER'] == ActionEnum.ANSWER
    assert ActionEnum['INVOKE_AGENT'] == ActionEnum.INVOKE_AGENT
    assert ActionEnum['INVOKE_AGENT_EXISTING_SESSION'] == ActionEnum.INVOKE_AGENT_EXISTING_SESSION
    assert ActionEnum['EXECUTE_COMMAND'] == ActionEnum.EXECUTE_COMMAND
    assert ActionEnum['APPEND_TO_AGENT_OUTPUT_INDEX'] == ActionEnum.APPEND_TO_AGENT_OUTPUT_INDEX
    assert ActionEnum['READ_AGENT_OUTPUT_INDEX'] == ActionEnum.READ_AGENT_OUTPUT_INDEX
    assert ActionEnum['FETCH_RECIPES'] == ActionEnum.FETCH_RECIPES
    assert ActionEnum['RUN_SERVER'] == ActionEnum.RUN_SERVER
    assert ActionEnum['CREATE_PROJECT_FILE'] == ActionEnum.CREATE_PROJECT_FILE
    assert ActionEnum['CREATE_AGENT_OUTPUT_FILE'] == ActionEnum.CREATE_AGENT_OUTPUT_FILE
    assert ActionEnum['GENERATE_STEPS'] == ActionEnum.GENERATE_STEPS
    assert ActionEnum['PROBLEM_STATEMENT'] == ActionEnum.PROBLEM_STATEMENT
    assert ActionEnum['INFER'] == ActionEnum.INFER
    assert ActionEnum['INFORM'] == ActionEnum.INFORM
    assert ActionEnum['OUTPUT'] == ActionEnum.OUTPUT
    assert ActionEnum['QUESTION'] == ActionEnum.QUESTION
    assert ActionEnum['RESPONSE'] == ActionEnum.RESPONSE
    assert ActionEnum['SOLUTION_COMPLETE'] == ActionEnum.SOLUTION_COMPLETE
    assert ActionEnum['STEPS'] == ActionEnum.STEPS
    assert ActionEnum['TRAIN_USING_SEARCH_TERM'] == ActionEnum.TRAIN_USING_SEARCH_TERM
    assert ActionEnum['TRAIN_USING_URL'] == ActionEnum.TRAIN_USING_URL
    assert ActionEnum['FEEDBACK'] == ActionEnum.FEEDBACK
    assert ActionEnum['TRAINING_OUTPUT'] == ActionEnum.TRAINING_OUTPUT
    assert ActionEnum['READ_PROJECT_FILES'] == ActionEnum.READ_PROJECT_FILES
    assert ActionEnum['READ_AGENT_OUTPUT_FILES'] == ActionEnum.READ_AGENT_OUTPUT_FILES
    assert ActionEnum['FIND_AND_REPLACE'] == ActionEnum.FIND_AND_REPLACE
    assert ActionEnum['INSERT_TEXT'] == ActionEnum.INSERT_TEXT
    assert ActionEnum['EXTRACT_DEPENDENCIES'] == ActionEnum.EXTRACT_DEPENDENCIES