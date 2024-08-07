import os
from openai import OpenAI

from sirji_tools.logger import create_logger 
from .base import CleanupBase
from ...decorators import retry_on_exception

class OpenAICleanup(CleanupBase):
    def __init__(self):      
        self.logger = create_logger("researcher.log", "debug")
        api_key = os.environ.get("SIRJI_MODEL_PROVIDER_API_KEY")

        if api_key is None:
            raise ValueError(
                "OpenAI API key is not set as an environment variable")

        # Initialize OpenAI client
        client = OpenAI(api_key=api_key, timeout=60)

        self.logger.info("Completed initializing OpenAI client")
        self.client = client

    @retry_on_exception()
    def delete_assistant(self, assistant_id):
        self.logger.info("Deleting assistant")
        try:
            response = self.client.beta.assistants.delete(assistant_id)
            print(response)
            self.logger.info(response)
        except Exception as e:
            print(e)
            self.logger.error(e)

    @retry_on_exception()
    def delete_vector_store(self, vector_store_id):
        try:
            response = self.client.beta.vector_stores.delete(
            vector_store_id = vector_store_id
            )
            print(response)
            self.logger.info(response)
        except Exception as e:
            print(e)
            self.logger.error(e)

    @retry_on_exception()
    def delete_file(self, file_path):
        try:
            response = self.client.files.delete(file_path)
            print(response)
            self.logger.info(response)
        except Exception as e:
            print(e)
            self.logger.error(e)

    @retry_on_exception()
    def delete_thread(self, thread_id):
        try:
            response = self.client.beta.threads.delete(thread_id = thread_id)
            print(response)
            self.logger.info(response)
        except Exception as e:
            print(e)
            self.logger.error(e)