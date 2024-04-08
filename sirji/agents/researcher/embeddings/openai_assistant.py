import json
import os

from sirji.config.model import ModelClient
from sirji.tools.logger import researcher as logger

from .base import BaseEmbeddings


class OpenAIAssistantEmbeddings(BaseEmbeddings):
    def __init__(self):
        logger.info("Initializing OpenAI Assistant Embeddings")

        # Initialize ModelClient
        model_client = ModelClient()

        # Set self.client as the value of self.client set in ModelClient class
        self.client = model_client.client
        self.model = model_client.model

        # Create assistant and preserve assistant_id
        self.assistant_id = self._create_assistant()

        self.index_file_path = "workspace/researcher/file_index.json"

        # Load or initialize the index file
        self.index_data = self._load_or_initialize_index_file()

        logger.info("Completed initializing OpenAI Assistant Embeddings")

    def index(self, folder_path):
        logger.info(f"Indexing files in the folder: {folder_path}")

        """
        Index files in the specified folder.
        """
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Check if file is not already indexed
            if os.path.isfile(file_path) and not any(
                d["local_path"] == file_path for d in self.index_data
            ):
                with open(file_path, "rb") as file_to_upload:
                    # Upload file to OpenAI
                    response = self._upload_file(file_to_upload)
                    if response.status == "processed":
                        file_id = response.id
                        # Associate file with assistant
                        associate_response = self._associate_file(file_id)
                        if not associate_response.id:
                            logger.error(
                                f"Failed to associate file {filename} with assistant."
                            )
                            continue
                        self.index_data.append(
                            {"local_path": file_path, "file_id": file_id}
                        )
                        self._update_index_file()
                    else:
                        logger.error(
                            f"Failed to upload file {filename}. Status Code: {response.status_code}"
                        )

        logger.info(f"Completed indexing files in the folder: {folder_path}")

    def retrieve_context(self, problem_statement):
        """
        Retrieve context using embeddings match for a problem statement.
        For OpenAI Assistants API, this step is not needed.
        To re-use the assistant_id, pass it in the retrieved context.
        """
        return self.assistant_id

    def _create_assistant(self):
        logger.info("Creating a new assistant instance")
        """
        Create a new assistant
        """
        assistant = self.client.beta.assistants.create(
            name="Research Assistant",
            instructions="As a research assistant, your task is to address problem statements programmatically. In your response, include code examples, GitHub URLs, relevant external URLs based on your trained knowledge. Also, if knowledge on additional terms is needed, mention them in your response. Avoid providing fabricated information if uncertain.",
            tools=[{"type": "retrieval"}],
            model=self.model,
        )

        logger.info("Completed creating a new assistant")
        return assistant.id

    def _load_or_initialize_index_file(self):
        logger.info("Initializing the index file")
        """
        Load or initialize the index file.
        """
        if os.path.exists(self.index_file_path):
            with open(self.index_file_path, "r") as index_file:
                return json.load(index_file)
        else:
            return []

    def _update_index_file(self):
        logger.info("Updating the index file with current index data")
        """
        Update the index file with current index data.
        """
        with open(self.index_file_path, "w") as index_file:
            json.dump(self.index_data, index_file, indent=4)

    def _upload_file(self, file_to_upload):
        logger.info("Uploading file to OpenAI")
        """
        Upload file to OpenAI.
        """
        return self.client.files.create(file=file_to_upload, purpose="assistants")

    def _associate_file(self, file_id):
        logger.info(f"Associating {file_id} file with assistant")
        """
        Associate file with assistant.
        """
        return self.client.beta.assistants.files.create(
            assistant_id=self.assistant_id, file_id=file_id
        )
