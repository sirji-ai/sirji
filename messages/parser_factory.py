from acknowledge import AcknowledgeMessage
from answer import AnswerMessage
from execute_command import ExecuteCommandMessage
from create_file import CreateFileMessage
from generate_steps import GenerateStepsMessage
from problem_statement import ProblemStatementMessage
from infer import InferMessage
from inform import InformMessage
from install_package import InstallPackageMessage
from output import OutputMessage
from question import QuestionMessage
from response import ResponseMessage
from solution_complete import SolutionCompleteMessage
from step_completed import StepCompletedMessage
from step_started import StepStartedMessage
from steps import StepsMessage
from train_using_search_term import TrainUsingSearchTermMessage
from train_using_url import TrainUsingUrlMessage
from feedback import FeedbackMessage

class ParserFactory:
    
    @staticmethod
    def get_parser(action_type):
        if action_type == "acknowledge":
            return AcknowledgeMessage
        elif action_type == "answer":
            return AnswerMessage
        elif action_type == "execute-command":
            return ExecuteCommandMessage
        elif action_type == "create-file":
            return CreateFileMessage
        elif action_type == "generate-steps":
            return GenerateStepsMessage
        elif action_type == "problem-statement":
            return ProblemStatementMessage
        elif action_type == "infer":
            return InferMessage
        elif action_type == "inform":
            return InformMessage
        elif action_type == "install-package":
            return InstallPackageMessage
        elif action_type == "output":
            return OutputMessage
        elif action_type == "question":
            return QuestionMessage
        elif action_type == "response":
            return ResponseMessage
        elif action_type == "solution-complete":
            return SolutionCompleteMessage
        elif action_type == "step-completed":
            return StepCompletedMessage
        elif action_type == "step-started":
            return StepStartedMessage
        elif action_type == "steps":
            return StepsMessage
        elif action_type == "train-using-search-term":
            return TrainUsingSearchTermMessage
        elif action_type == "train-using-url":
            return TrainUsingUrlMessage
        elif action_type == "feedback":
            return FeedbackMessage
        else:
            raise Exception("Invalid action type: " + action_type)
