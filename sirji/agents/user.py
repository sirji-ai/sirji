from sirji.messages.problem_statement import ProblemStatementMessage


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
    def generate_problem_statement_message(self, problem_statement):
        pass

    def generate_ack_message(self, ack):
        pass

    def generate_answer_message(self, answer):
        pass
