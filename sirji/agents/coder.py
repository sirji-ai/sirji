from sirji.config.model import ModelClient
from sirji.prompts.coder import CoderPrompt
from sirji.tools.logger import coder as cLogger


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


class Coder(metaclass=SingletonMeta):
    def __init__(self):
        # Initialize conversation
        self.conversation = [
            {"role": "system", "content": CoderPrompt().system_prompt()}
        ]

        # Initialize ModelClient
        model_client = ModelClient()

        # Set self.client as the value of self.client set in ModelClient class
        self.client = model_client.client

    def message(self, input_message):
        # Append user's input message to the conversation
        self.conversation.append({"role": "user", "content": input_message})

        cLogger.info(f"Incoming: \n{input_message}")

        cLogger.info("Calling OpenAI Chat Completions API")

        chat_completion = self.client.chat.completions.create(
            messages=self.conversation,
            model="gpt-4-turbo-preview",
            temperature=0,
            max_tokens=4095,
        )

        response_message = chat_completion.choices[0].message.content

        self.conversation.append({"role": "assistant", "content": response_message})

        cLogger.info(f"Outgoing: \n{response_message}")
        return response_message
