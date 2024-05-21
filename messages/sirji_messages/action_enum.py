from enum import Enum, auto


class ActionEnum(Enum):
    ANSWER = auto()
    INVOKE_AGENT = auto()
    INVOKE_AGENT_EXISTING_SESSION = auto()
    EXECUTE_COMMAND = auto()
    APPEND_TO_AGENT_OUTPUT_INDEX = auto()
    READ_AGENT_OUTPUT_INDEX = auto()
    FETCH_RECIPE = auto()
    FETCH_RECIPE_INDEX = auto()
    RUN_SERVER = auto()
    CREATE_PROJECT_FILE = auto()
    CREATE_AGENT_OUTPUT_FILE = auto()
    GENERATE_STEPS = auto()
    PROBLEM_STATEMENT = auto()
    INFER = auto()
    INFORM = auto()
    OUTPUT = auto()
    QUESTION = auto()
    RESPONSE = auto()
    SOLUTION_COMPLETE = auto()
    STEPS = auto()
    TRAIN_USING_SEARCH_TERM = auto()
    TRAIN_USING_URL = auto()
    FEEDBACK = auto()
    TRAINING_OUTPUT = auto()
    READ_PROJECT_FILES = auto()
    READ_AGENT_OUTPUT_FILES = auto()
    FIND_AND_REPLACE = auto()
    INSERT_TEXT = auto()
    EXTRACT_DEPENDENCIES = auto()
    FIND_AND_REPLACE_IN_PROJECT = auto()
    SEARCH_FILE_IN_PROJECT = auto()
