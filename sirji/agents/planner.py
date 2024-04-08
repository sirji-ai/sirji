from sirji.config.model import ModelClient
from sirji.messages.parser import MessageParser
from sirji.prompts.planner import PlannerPrompt
from sirji.storage.steps import initialize_steps
from sirji.tools.logger import planner as pLogger


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


class Planner(metaclass=SingletonMeta):
    def __init__(self):
        # Initialize conversation
        self.conversation = [
            {
                "role": "system",
                "content": PlannerPrompt("Coding Agent", "Coder").system_prompt(),
            }
        ]

        # Initialize ModelClient
        model_client = ModelClient()

        # Set self.client as the value of self.client set in ModelClient class
        self.client = model_client.client
        self.model = model_client.model
        pass

    def message(self, input_message):
        # Append user's input message to the conversation
        self.conversation.append({"role": "user", "content": input_message})

        chat_completion = self.client.chat.completions.create(
            messages=self.conversation,
            model=self.model,
            temperature=0,
            max_tokens=4095,
        )

        response_message = chat_completion.choices[0].message.content

        # Storing
        self.store_steps(response_message)

        self.conversation.append({"role": "assistant", "content": response_message})
        return response_message

    def store_steps(self, message):
        steps = MessageParser.parse_steps(message)

        for index, description in enumerate(steps, start=1):
            pLogger.info(f"[ ] Step {index}: {description}")

        initialize_steps(steps)
