from enum import Enum, auto


class ActionEnum(Enum):
    ANSWER = auto()
    INVOKE_AGENT = auto()
    INVOKE_AGENT_EXISTING_SESSION = auto()
    EXECUTE_COMMAND = auto()
    APPEND_TO_SHARED_RESOURCES_INDEX = auto()
    READ_SHARED_RESOURCE_INDEX = auto()
    RUN_SERVER = auto()
    CREATE_PROJECT_FILE = auto()
    CREATE_SHARED_RESOURCE_FILE = auto()
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
    READ_SHARED_RESOURCES_FILES = auto()
    READ_DIR_STRUCTURE = auto()
    FIND_AND_REPLACE = auto()
    INSERT_TEXT = auto()
    EXTRACT_DEPENDENCIES = auto()
