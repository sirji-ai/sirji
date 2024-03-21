from openai import OpenAI
import os


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


class Executor(metaclass=SingletonMeta):
    def __init__(self):
        pass

    def message(self, input_message):
        # - outgoing
        #   - output response - output
        # - incoming
        #   - create file
                # - filename
                # - content
        #   - execute file
        #   - install package
        pass
