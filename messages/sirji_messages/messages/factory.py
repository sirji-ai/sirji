from sirji_messages import ActionEnum

# Import all the message classes
from .actions.acknowledge import AcknowledgeMessage
from .actions.answer import AnswerMessage
from .actions.execute_command import ExecuteCommandMessage
from .actions.create_file import CreateFileMessage
from .actions.generate_steps import GenerateStepsMessage
from .actions.problem_statement import ProblemStatementMessage
from .actions.infer import InferMessage
from .actions.inform import InformMessage
from .actions.install_package import InstallPackageMessage
from .actions.output import OutputMessage
from .actions.question import QuestionMessage
from .actions.response import ResponseMessage
from .actions.solution_complete import SolutionCompleteMessage
from .actions.step_completed import StepCompletedMessage
from .actions.step_started import StepStartedMessage
from .actions.steps import StepsMessage
from .actions.train_using_search_term import TrainUsingSearchTermMessage
from .actions.train_using_url import TrainUsingUrlMessage
from .actions.feedback import FeedbackMessage
from .actions.training_output import TrainingOutputMessage
from .actions.read_dir import ReadDirMessage
from .actions.read_file import ReadFileMessage


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
        ActionEnum.ACKNOWLEDGE: AcknowledgeMessage,
        ActionEnum.ANSWER: AnswerMessage,
        ActionEnum.EXECUTE_COMMAND: ExecuteCommandMessage,
        ActionEnum.CREATE_FILE: CreateFileMessage,
        ActionEnum.GENERATE_STEPS: GenerateStepsMessage,
        ActionEnum.PROBLEM_STATEMENT: ProblemStatementMessage,
        ActionEnum.INFER: InferMessage,
        ActionEnum.INFORM: InformMessage,
        ActionEnum.INSTALL_PACKAGE: InstallPackageMessage,
        ActionEnum.OUTPUT: OutputMessage,
        ActionEnum.QUESTION: QuestionMessage,
        ActionEnum.RESPONSE: ResponseMessage,
        ActionEnum.SOLUTION_COMPLETE: SolutionCompleteMessage,
        ActionEnum.STEP_COMPLETED: StepCompletedMessage,
        ActionEnum.STEP_STARTED: StepStartedMessage,
        ActionEnum.STEPS: StepsMessage,
        ActionEnum.TRAIN_USING_SEARCH_TERM: TrainUsingSearchTermMessage,
        ActionEnum.TRAIN_USING_URL: TrainUsingUrlMessage,
        ActionEnum.FEEDBACK: FeedbackMessage,
        ActionEnum.TRAINING_OUTPUT: TrainingOutputMessage,
        ActionEnum.READ_DIR: ReadDirMessage,
        ActionEnum.READ_FILE: ReadFileMessage
    }

