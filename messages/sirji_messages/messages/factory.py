from sirji_messages import ActionEnum

# Import all the message classes
from .actions.execute_command import ExecuteCommandMessage
from .actions.run_server import RunServerMessage
from .actions.create_file import CreateFileMessage
from .actions.infer import InferMessage
from .actions.question import QuestionMessage
from .actions.response import ResponseMessage
from .actions.solution_complete import SolutionCompleteMessage
from .actions.train_using_search_term import TrainUsingSearchTermMessage
from .actions.train_using_url import TrainUsingUrlMessage
from .actions.read_dir import ReadDirMessage
from .actions.read_dir_structure import ReadDirStructureMessage
from .actions.read_files import ReadFilesMessage
from .actions.append_to_shared_resource_index import AppendToSharedResourceIndexMessage
from .actions.read_shared_resource_index import ReadSharedResourceIndexMessage


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
        ActionEnum.EXECUTE_COMMAND: ExecuteCommandMessage,
        ActionEnum.RUN_SERVER: RunServerMessage,
        ActionEnum.CREATE_FILE: CreateFileMessage,
        ActionEnum.INFER: InferMessage,
        ActionEnum.QUESTION: QuestionMessage,
        ActionEnum.RESPONSE: ResponseMessage,
        ActionEnum.SOLUTION_COMPLETE: SolutionCompleteMessage,
        ActionEnum.TRAIN_USING_SEARCH_TERM: TrainUsingSearchTermMessage,
        ActionEnum.TRAIN_USING_URL: TrainUsingUrlMessage,
        ActionEnum.READ_DIR: ReadDirMessage,
        ActionEnum.READ_FILES: ReadFilesMessage,
        ActionEnum.READ_DIR_STRUCTURE: ReadDirStructureMessage,
        ActionEnum.APPEND_TO_SHARED_RESOURCES_INDEX: AppendToSharedResourceIndexMessage,
        ActionEnum.READ_SHARED_RESOURCE_INDEX: ReadSharedResourceIndexMessage
    }

