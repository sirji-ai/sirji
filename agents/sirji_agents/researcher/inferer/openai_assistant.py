import os
import time
from openai import OpenAI

from sirji_tools.logger import create_logger 

# Assuming .base contains your ResearcherInfererBase
from .base import ResearcherInfererBase


class OpenAIAssistantInferer(ResearcherInfererBase):
    def __init__(self, init_payload):
        self.logger = create_logger("researcher.log", "debug")
        self.logger.info("Initializing OpenAI Assistant Inferer")
        """
        Initializes the OpenAIAssistantInferer by setting up the OpenAI client 
        with the API key obtained from environment variables.
        """

        self.init_payload = init_payload

        # Fetch OpenAI API key from an environment variable
        api_key = os.environ.get("SIRJI_MODEL_PROVIDER_API_KEY")

        if api_key is None:
            raise ValueError(
                "OpenAI API key is not set as an environment variable")

        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)

        # Ensure assistant_id is provided in init_payload
        if 'assistant_id' not in self.init_payload:
            raise ValueError("assistant_id must be provided in init_payload")

        # Reading the assistant ID from init_payload
        self.assistant_id = self.init_payload['assistant_id']

        self.logger.info("Completed initializing OpenAI Assistant Inferer")

    def infer(self, problem_statement):
        self.logger.info("Started inferring using OpenAI Assistant Inferer")

        """
        Infers an answer by calling a chat model using the retrieved context and the problem statement.

        :param retrieved_context: The context information retrieved based on embeddings match.
        :param problem_statement: The initial problem statement or query.
        :return: A tuple containing the model's response based on the combined information of the problem statement & the retrieved context, the number of prompt tokens used in the run, and the number of completion tokens used in the run.
        """

        # Send the generated prompt to the assistant
        # self.client.beta.threads.messages.create(
        #     thread_id=self.thread_id,
        #     role="user",
        #     content=problem_statement,
        # )

        try:
            thread = self.client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": problem_statement
                    }
                ]
            )
            self.thread_id = thread.id
            self.logger.info("Completed inferring using OpenAI Assistant Inferer")
            
            # Fetch and return the assistant's response

            response = self._fetch_response()
        except Exception as e:
            self.logger.error("An error occurred during inference: %s", str(e))
            response = 'An error occurred during inference', 0, 0
        finally:
            if self.thread_id:
                try:
                    deleteResponse = self.client.beta.threads.delete(thread_id=self.thread_id)
                    self.logger.info("Thread deleted successfully: %s", deleteResponse)
                    print('deleteResponse', deleteResponse)
                except Exception as delete_e:
                    self.logger.error("Failed to delete thread: %s", str(delete_e))
                print('self.thread_id', self.thread_id)
        
        return response



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
        self.logger.info("Fetching response using OpenAI Assistant Inferer")

        """
        Initiates a run and waits for the assistant's response, then retrieves and returns the last message.

        :return: A tuple containing the text of the assistant's latest message, the number of prompt tokens used in the run, and the number of completion tokens used in the run.
        """
        
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread_id, assistant_id=self.assistant_id
        )


        messages = list(self.client.beta.threads.messages.list(thread_id=self.thread_id, run_id=run.id))

        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = self.client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))

        return message_content.value, run.usage.prompt_tokens, run.usage.completion_tokens