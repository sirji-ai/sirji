from sirji_messages import ActionEnum

# Import all the message classes
from .actions.execute_command import ExecuteCommandMessage
from .actions.run_server import RunServerMessage
from .actions.create_project_file import CreateProjectFileMessage
from .actions.create_agent_output_file import CreateAgentOutputFileMessage
from .actions.infer import InferMessage
from .actions.question import QuestionMessage
from .actions.response import ResponseMessage
from .actions.solution_complete import SolutionCompleteMessage
from .actions.train_using_search_term import TrainUsingSearchTermMessage
from .actions.train_using_url import TrainUsingUrlMessage
from .actions.read_project_files import ReadProjectFilesMessage
from .actions.read_agent_output_files import ReadAgentOutputFilesMessage
from .actions.append_to_agent_output_index import AppendToAgentOutputIndexMessage
from .actions.read_agent_output_index import ReadAgentOutputIndexMessage
from .actions.invoke_agent import InvokeAgentMessage
from .actions.invoke_agent_existing_session import InvokeAgentExistingSessionMessage
from .actions.find_and_replace import FindAndReplace
from .actions.insert_text import InsertText
from .actions.extract_dependencies import ExtractDependenciesMessage


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
        ActionEnum.CREATE_AGENT_OUTPUT_FILE: CreateAgentOutputFileMessage,
        ActionEnum.INFER: InferMessage,
        ActionEnum.QUESTION: QuestionMessage,
        ActionEnum.RESPONSE: ResponseMessage,
        ActionEnum.SOLUTION_COMPLETE: SolutionCompleteMessage,
        ActionEnum.TRAIN_USING_SEARCH_TERM: TrainUsingSearchTermMessage,
        ActionEnum.TRAIN_USING_URL: TrainUsingUrlMessage,
        ActionEnum.READ_PROJECT_FILES: ReadProjectFilesMessage,
        ActionEnum.READ_AGENT_OUTPUT_FILES: ReadAgentOutputFilesMessage,
        ActionEnum.APPEND_TO_AGENT_OUTPUT_INDEX: AppendToAgentOutputIndexMessage,
        ActionEnum.READ_AGENT_OUTPUT_INDEX: ReadAgentOutputIndexMessage,
        ActionEnum.FIND_AND_REPLACE: FindAndReplace,
        ActionEnum.INSERT_TEXT: InsertText,
        ActionEnum.EXTRACT_DEPENDENCIES: ExtractDependenciesMessage
    }

