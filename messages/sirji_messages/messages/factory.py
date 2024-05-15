from sirji_messages import ActionEnum

# Import all the message classes
from .actions.execute_command import ExecuteCommandMessage
from .actions.run_server import RunServerMessage
from .actions.create_workspace_file import CreateWorkspaceFileMessage
from .actions.create_shared_resource_file import CreateSharedResourceFileMessage
from .actions.infer import InferMessage
from .actions.question import QuestionMessage
from .actions.response import ResponseMessage
from .actions.solution_complete import SolutionCompleteMessage
from .actions.train_using_search_term import TrainUsingSearchTermMessage
from .actions.train_using_url import TrainUsingUrlMessage
from .actions.read_dir_structure import ReadDirStructureMessage
from .actions.read_workspace_files import ReadWorkspaceFilesMessage
from .actions.read_shared_resources_files import ReadSharedResourcesFilesMessage
from .actions.append_to_shared_resource_index import AppendToSharedResourceIndexMessage
from .actions.read_shared_resource_index import ReadSharedResourceIndexMessage
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
        ActionEnum.CREATE_WORKSPACE_FILE: CreateWorkspaceFileMessage,
        ActionEnum.CREATE_SHARED_RESOURCE_FILE: CreateSharedResourceFileMessage,
        ActionEnum.INFER: InferMessage,
        ActionEnum.QUESTION: QuestionMessage,
        ActionEnum.RESPONSE: ResponseMessage,
        ActionEnum.SOLUTION_COMPLETE: SolutionCompleteMessage,
        ActionEnum.TRAIN_USING_SEARCH_TERM: TrainUsingSearchTermMessage,
        ActionEnum.TRAIN_USING_URL: TrainUsingUrlMessage,
        ActionEnum.READ_WORKSPACE_FILES: ReadWorkspaceFilesMessage,
        ActionEnum.READ_SHARED_RESOURCES_FILES: ReadSharedResourcesFilesMessage,
        ActionEnum.READ_DIR_STRUCTURE: ReadDirStructureMessage,
        ActionEnum.APPEND_TO_SHARED_RESOURCES_INDEX: AppendToSharedResourceIndexMessage,
        ActionEnum.READ_SHARED_RESOURCE_INDEX: ReadSharedResourceIndexMessage,
        ActionEnum.FIND_AND_REPLACE: FindAndReplace,
        ActionEnum.INSERT_TEXT: InsertText,
        ActionEnum.EXTRACT_DEPENDENCIES: ExtractDependenciesMessage
    }

