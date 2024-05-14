import os
import time
from openai import OpenAI

from sirji_tools.logger import r_logger as logger

# Assuming .base contains your ResearcherInfererBase
from .base import ResearcherInfererBase


class OpenAIAssistantInferer(ResearcherInfererBase):
    def __init__(self, init_payload):
        logger.info("Initializing OpenAI Assistant Inferer")
        """
        Initializes the OpenAIAssistantInferer by setting up the OpenAI client 
        with the API key obtained from environment variables.
        """

        self.init_payload = init_payload

        # Fetch OpenAI API key from an environment variable
        api_key = os.environ.get("SIRJI_OPENAI_API_KEY")

        if api_key is None:
            raise ValueError(
                "OpenAI API key is not set as an environment variable")

        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)

        # Reading the assistant ID from init_payload
        self.assistant_id = self.init_payload['assistant_id']

        if 'thread_id' not in self.init_payload or not self.init_payload['thread_id']:
            assistant = self.client.beta.assistants.retrieve(
                self.assistant_id)
            thread = self.client.beta.threads.create()
            self.init_payload['thread_id'] = thread.id

        logger.info("Completed initializing OpenAI Assistant Inferer")

    def infer(self, retrieved_context, problem_statement):
        logger.info("Started inferring using OpenAI Assistant Inferer")

        """
        Infers an answer by calling a chat model using the retrieved context and the problem statement.

        :param retrieved_context: The context information retrieved based on embeddings match.
        :param problem_statement: The initial problem statement or query.
        :return: A tuple containing the model's response based on the combined information of the problem statement & the retrieved context, the number of prompt tokens used in the run, and the number of completion tokens used in the run.
        """

        # Generate a prompt to send to the assistant
        prompt = self.generate_prompt(retrieved_context, problem_statement)

        # Send the generated prompt to the assistant
        self.client.beta.threads.messages.create(
            thread_id=self.init_payload['thread_id'],
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

    def _fetch_response(self):
        logger.info("Fetching response using OpenAI Assistant Inferer")

        """
        Initiates a run and waits for the assistant's response, then retrieves and returns the last message.

        :return: A tuple containing the text of the assistant's latest message, the number of prompt tokens used in the run, and the number of completion tokens used in the run.
        """
        # Start a run to fetch the assistant's response
        run = self.client.beta.threads.runs.create(
            thread_id=self.init_payload['thread_id'],
            assistant_id=self.assistant_id,
            model="gpt-4o",
            tools=[{"type": "retrieval"}]
        )

        logger.info(
            "Completed fetching response using OpenAI Assistant Inferer")
        

        # Loop until the run status is 'completed'
        while run.status != "completed":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.init_payload['thread_id'], run_id=run.id)
            
            time.sleep(1)  # Sleep to prevent overwhelming the API

        # Retrieve and return the last message content from the thread
        messages = self.client.beta.threads.messages.list(
            thread_id=self.init_payload['thread_id'])
        new_message = messages.data[0].content[0].text.value
        return new_message, run.usage.prompt_tokens, run.usage.completion_tokens
