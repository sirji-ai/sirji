import time

from sirji.config.model import ModelClient
from sirji.tools.logger import researcher as logger

# Assuming .base contains your ResearcherInfererBase
from .base import ResearcherInfererBase


class OpenAIAssistantInferer(ResearcherInfererBase):
    def __init__(self):
        logger.info("Initializing OpenAI Assistant Inferer")
        """
        Initializes the OpenAIAssistantInferer by setting up the OpenAI client 
        with the API key obtained from environment variables.
        """
        # Initialize ModelClient
        model_client = ModelClient()

        # Set self.client as the value of self.client set in ModelClient class
        self.client = model_client.client

        # Placeholder for the OpenAI Assistant object
        self.assistant = None
        # Placeholder for storing the current assistant's ID
        self.assistant_id = None
        # Placeholder for the conversation thread with the assistant
        self.thread = None

        logger.info("Completed initializing OpenAI Assistant Inferer")

    def infer(self, retrieved_context, problem_statement):
        logger.info("Started inferring using OpenAI Assistant Inferer")

        """
        Infers an answer by calling a chat model using the retrieved context and the problem statement.

        :param retrieved_context: The context information retrieved based on embeddings match.
        :param problem_statement: The initial problem statement or query.
        :return: The model's response based on the combined information of the problem statement and the retrieved context.
        """

        # Note: In this case, the assistant id is passed as retrieved context.
        assistant_id = retrieved_context

        # Setup assistant if not already created or if the assistant_id has changed.
        self._set_assistant(assistant_id)

        # Generate a prompt to send to the assistant
        prompt = self.generate_prompt(retrieved_context, problem_statement)

        # Send the generated prompt to the assistant
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=prompt,
        )

        logger.info("Completed inferring using OpenAI Assistant Inferer")

        # Fetch and return the assistant's response
        return self._fetch_response()

    def generate_prompt(self, retrieved_context, problem_statement):
        """
        Generates a prompt by combining the problem statement and the retrieved context.

        :param retrieved_context: Context information retrieved based on embeddings match.
        :param problem_statement: The initial problem statement or query.
        :return: A prompt string that combines both the problem statement and the retrieved context.
        """
        # This basic implementation simply returns the problem_statement.
        # Customize this method to combine problem_statement and retrieved_context into a coherent prompt.
        return problem_statement

    def _set_assistant(self, assistant_id):
        logger.info("Setting up OpenAI Assistant Inferer")
        """
        Ensures the assistant object is set up correctly, creating a new assistant 
        and thread if the assistant ID changes or isn't set yet.

        :param assistant_id: The OpenAI Assistant ID to be used.
        """
        if not self.assistant or self.assistant_id != assistant_id:
            self.assistant_id = assistant_id
            self.assistant = self.client.beta.assistants.retrieve(assistant_id)
            # Create a new conversation thread with the assistant
            self.thread = self.client.beta.threads.create()

        logger.info("Completed setting up OpenAI Assistant Inferer")

    def _fetch_response(self):
        logger.info("Fetching response using OpenAI Assistant Inferer")

        """
        Initiates a run and waits for the assistant's response, then retrieves and returns the last message.

        :return: The text of the assistant's latest message.
        """
        # Start a run to fetch the assistant's response
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant_id,
            model="gpt-4-turbo-preview",
            tools=[{"type": "retrieval"}],
        )

        logger.info("Completed fetching response using OpenAI Assistant Inferer")

        # Loop until the run status is 'completed'
        while run.status != "completed":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id, run_id=run.id
            )
            time.sleep(1)  # Sleep to prevent overwhelming the API

        # Retrieve and return the last message content from the thread
        messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
        new_message = messages.data[0].content[0].text.value
        return new_message
