import os
from openai import OpenAI
import time

# Assuming .base contains your ResearcherInfererBase
from .base import ResearcherInfererBase


class OpenAIAssistantInferer(ResearcherInfererBase):
    def __init__(self):
        """
        Initializes the OpenAIAssistantInferer by setting up the OpenAI client 
        with the API key obtained from environment variables.
        """
        # Fetch OpenAI API key from an environment variable
        api_key = os.environ.get(
            "SIRJI_OPENAI_API_KEY", "<your OpenAI API key if not set as env var>")

        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        
        # Placeholder for the OpenAI Assistant object
        self.assistant = None
        # Placeholder for storing the current assistant's ID
        self.assistant_id = None
        # Placeholder for the conversation thread with the assistant
        self.thread = None

    def infer(self, retrieved_context, problem_statement):
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

    def _fetch_response(self):
        """
        Initiates a run and waits for the assistant's response, then retrieves and returns the last message.

        :return: The text of the assistant's latest message.
        """
        # Start a run to fetch the assistant's response
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant_id,
            model="gpt-4-turbo-preview",
            tools=[{"type": "retrieval"}]
        )

        # Loop until the run status is 'completed'
        while run.status != "completed":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id, run_id=run.id)
            time.sleep(1)  # Sleep to prevent overwhelming the API

        # Retrieve and return the last message content from the thread
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id)
        new_message = messages.data[0].content[0].text.value
        return new_message
