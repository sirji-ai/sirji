import pytest
from sirji_messages import ActionEnum
from sirji_messages.messages.factory import MessageFactory

# Here we're importing specific message classes for comparison
from sirji_messages.messages.actions.acknowledge import AcknowledgeMessage
from sirji_messages.messages.actions.question import QuestionMessage
from sirji_messages.messages.actions.inform import InformMessage
from sirji_messages.messages.actions.problem_statement import ProblemStatementMessage

# Test Cases for MessageFactory


def test_message_factory_acknowledge():
    assert isinstance(MessageFactory[ActionEnum.ACKNOWLEDGE.name](
    ), AcknowledgeMessage), "Incorrect message class for ACKNOWLEDGE action"


def test_message_factory_question():
    assert isinstance(MessageFactory[ActionEnum.QUESTION.name](
    ), QuestionMessage), "Incorrect message class for QUESTION action"


def test_message_factory_inform():
    assert isinstance(MessageFactory[ActionEnum.INFORM.name](
    ), InformMessage), "Incorrect message class for INFORM action"


def test_message_factory_problem_statement():
    assert isinstance(MessageFactory[ActionEnum.PROBLEM_STATEMENT.name](
    ), ProblemStatementMessage), "Incorrect message class for PROBLEM_STATEMENT action"

# Optionally, you could add tests to verify the correct behavior or outputs of these messages or their methods.
# For example, you could test the generation of sample messages, ensuring it matches expected formats.
