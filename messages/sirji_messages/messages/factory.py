from sirji_messages import ActionEnum

# Import all the message classes
from .actions.execute_command import ExecuteCommandMessage
from .actions.run_server import RunServerMessage
from .actions.create_project_file import CreateProjectFileMessage
from .actions.infer import InferMessage
from .actions.question import QuestionMessage
from .actions.response import ResponseMessage
from .actions.solution_complete import SolutionCompleteMessage
from .actions.train_using_search_term import TrainUsingSearchTermMessage
from .actions.train_using_url import TrainUsingUrlMessage
from .actions.read_project_files import ReadProjectFilesMessage
from .actions.read_agent_output_files import ReadAgentOutputFilesMessage
from .actions.read_agent_output_index import ReadAgentOutputIndexMessage
from .actions.invoke_agent import InvokeAgentMessage
from .actions.invoke_agent_existing_session import InvokeAgentExistingSessionMessage
from .actions.find_and_replace import FindAndReplace
from .actions.extract_dependencies import ExtractDependenciesMessage
from .actions.search_code_in_project import SearchCodeInProject
from .actions.fetch_recipe import FetchRecipeMessage
from .actions.fetch_recipe_index import FetchRecipeIndexMessage
from .actions.insert_above import InsertAbove
from .actions.insert_below import InsertBelow
from .actions.store_in_scratch_pad import StoreInScratchPad
from .actions.store_in_agent_output import StoreInAgentOutputMessage
from .actions.log_steps import LogSteps
from .actions.sync_codebase import SyncCodebase
from .actions.create_assistant import CreateAssistantMessage


class MetaMessageFactory(type):
    def __getitem__(cls, action):
        try:
            action_type = ActionEnum[action]
            return cls._message_map[action_type]
        except KeyError as e:
            raise AttributeError(
                f"{action} not found in MessageFactory or ActionType Enum.") from e

# Use the metaclass for our factory


class MessageFactory(metaclass=MetaMessageFactory):

    # Map ActionTypes to their respective message classes
    _message_map = {
        ActionEnum.INVOKE_AGENT: InvokeAgentMessage,
        ActionEnum.INVOKE_AGENT_EXISTING_SESSION: InvokeAgentExistingSessionMessage,
        ActionEnum.EXECUTE_COMMAND: ExecuteCommandMessage,
        ActionEnum.RUN_SERVER: RunServerMessage,
        ActionEnum.CREATE_PROJECT_FILE: CreateProjectFileMessage,
        ActionEnum.INFER: InferMessage,
        ActionEnum.QUESTION: QuestionMessage,
        ActionEnum.RESPONSE: ResponseMessage,
        ActionEnum.SOLUTION_COMPLETE: SolutionCompleteMessage,
        ActionEnum.TRAIN_USING_SEARCH_TERM: TrainUsingSearchTermMessage,
        ActionEnum.TRAIN_USING_URL: TrainUsingUrlMessage,
        ActionEnum.READ_PROJECT_FILES: ReadProjectFilesMessage,
        ActionEnum.READ_AGENT_OUTPUT_FILES: ReadAgentOutputFilesMessage,
        ActionEnum.STORE_IN_AGENT_OUTPUT: StoreInAgentOutputMessage,
        ActionEnum.READ_AGENT_OUTPUT_INDEX: ReadAgentOutputIndexMessage,
        ActionEnum.FIND_AND_REPLACE: FindAndReplace,
        ActionEnum.INSERT_ABOVE: InsertAbove,
        ActionEnum.INSERT_BELOW: InsertBelow,
        ActionEnum.EXTRACT_DEPENDENCIES: ExtractDependenciesMessage,
        ActionEnum.SEARCH_CODE_IN_PROJECT: SearchCodeInProject,
        ActionEnum.FETCH_RECIPE: FetchRecipeMessage,
        ActionEnum.FETCH_RECIPE_INDEX: FetchRecipeIndexMessage,
        ActionEnum.STORE_IN_SCRATCH_PAD: StoreInScratchPad,
        ActionEnum.LOG_STEPS: LogSteps,
        ActionEnum.SYNC_CODEBASE: SyncCodebase,
        ActionEnum.CREATE_ASSISTANT: CreateAssistantMessage
    }

