import sys 

from sirji.messages.problem_statement import ProblemStatementMessage
from sirji.messages.acknowledge import AcknowledgeMessage
from sirji.prompts.user import UserPrompt

from sirji.messages.parser import MessageParser

from sirji.tools.logger import user as logger


class SingletonMeta(type):
    """
    This is a metaclass that will be used to create a Singleton class.
    It ensures that only one instance of the Singleton class exists.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # If an instance of the class does not exist, create one; otherwise, return the existing one.
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class User(metaclass=SingletonMeta):
    def generate_problem_statement_message(self, problem_statement, for_user):
        user = UserPrompt(for_user, '')
        problem_statement_message = ProblemStatementMessage(for_user)

        return problem_statement_message.generate(user.name(), {
            "details": problem_statement
        })   
    
    def message(self, input_message):     
        parsed_message = MessageParser.parse(input_message)

        action = parsed_message.get("ACTION")
        from_user = parsed_message.get("FROM")
        to_user = parsed_message.get("TO")

        if action == "step-started":
            logger.info(f"Step started: {parsed_message.get('DETAILS')}")
            return AcknowledgeMessage(to_user).generate(from_user, {})
        elif action == "step-completed":
            logger.info(f"Step completed: {parsed_message.get('DETAILS')}")
            return AcknowledgeMessage(to_user).generate(from_user, {})
        elif action == "solution-complete":
            logger.info(f"Solution completed: {parsed_message.get('DETAILS')}")
            logger.info("Exiting.")
            sys.exit(0)
   