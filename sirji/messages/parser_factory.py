from sirji.messages.acknowledge import AcknowledgeMessage
from sirji.messages.answer import AnswerMessage
from sirji.messages.execute_file import ExecuteFileMessage
from sirji.messages.create_file import CreateFileMessage
from sirji.messages.elaborated_problem_statement import ElaboratedProblemStatementMessage
from sirji.messages.problem_statement import ProblemStatementMessage
from sirji.messages.infer import InferMessage
from sirji.messages.inform import InformMessage
from sirji.messages.install_package import InstallPackageMessage
from sirji.messages.output import OutputMessage
from sirji.messages.question import QuestionMessage
from sirji.messages.response import ResponseMessage
from sirji.messages.solution_complete import SolutionCompleteMessage
from sirji.messages.step_completed import StepCompletedMessage
from sirji.messages.step_started import StepStartedMessage
from sirji.messages.steps import StepsMessage
from sirji.messages.train_using_search_term import TrainUsingSearchTermMessage
from sirji.messages.train_using_url import TrainUsingUrlMessage

class ParserFactory:
    
    @staticmethod
    def get_parser(action_type):
        if action_type == "acknowledge":
            return AcknowledgeMessage
        elif action_type == "answer":
            return AnswerMessage
        elif action_type == "execute-file":
            return ExecuteFileMessage
        elif action_type == "create-file":
            return CreateFileMessage
        elif action_type == "elaborated-problem-statement":
            return ElaboratedProblemStatementMessage
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
        else:
            raise Exception("Invalid action type: " + action_type)
