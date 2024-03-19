import os
import requests
import json
from openai import OpenAI
from .base import BaseEmbeddings


class OpenAIAssistantEmbeddings(BaseEmbeddings):

    def __init__(self):
        # Fetch OpenAI API key from environment variable
        self.api_key = os.environ.get(
            "SIRJI_OPENAI_API_KEY", "<your OpenAI API key if not set as env var>")

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

        # Create assistant and preserve assistant_id
        self.assistant_id = self.create_assistant()

        self.index_file_path = 'workspace/researcher/file_index.json'

        # Load or initialize the index file
        self.index_data = self.load_or_initialize_index_file()

    def create_assistant(self):
        """
        Create a new assistant
        """
        # Create a new assistant if not found
        assistant = self.client.beta.assistants.create(
            name="Research Assistant",
            instructions="You are a research assistant who uses the indexed knowledge to answer specific questions based on the knowledge. If you do not know, do not make up facts by yourself.",
            tools=[{"type": "retrieval"}],
            model="gpt-4-turbo-preview",
        )
        return assistant.id

    def load_or_initialize_index_file(self):
        """
        Load or initialize the index file.
        """
        if os.path.exists(self.index_file_path):
            with open(self.index_file_path, 'r') as index_file:
                return json.load(index_file)
        else:
            return []

    def update_index_file(self):
        """
        Update the index file with current index data.
        """
        with open(self.index_file_path, 'w') as index_file:
            json.dump(self.index_data, index_file, indent=4)

    def index(self, folder_path):
        """
        Index files in the specified folder.
        """
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Check if file is not already indexed
            if os.path.isfile(file_path) and not any(d['local_path'] == file_path for d in self.index_data):
                with open(file_path, 'rb') as file_to_upload:
                    # Upload file to OpenAI
                    response = self.upload_file(file_to_upload)

                    if response.status == 'processed':
                        file_id = response.id
                        # Associate file with assistant
                        associate_response = self.associate_file(file_id)

                        if not associate_response.id:
                            print(
                                f"Failed to associate file {filename} with assistant.")
                            continue
                        self.index_data.append(
                            {'local_path': file_path, 'file_id': file_id})
                        self.update_index_file()
                    else:
                        print(
                            f"Failed to upload file {filename}. Status Code: {response.status_code}")

    def upload_file(self, file_to_upload):
        """
        Upload file to OpenAI.
        """
        return self.client.files.create(
            file=file_to_upload,
            purpose='assistants'
        )

    def associate_file(self, file_id):
        """
        Associate file with assistant.
        """
        return self.client.beta.assistants.files.create(
            assistant_id=self.assistant_id, file_id=file_id)

    def retrieve_context(self, problem_statement):
        """
        Retrieve context using embeddings match for a problem statement.
        For OpenAI Assistants API, this step is not needed.
        To re-use the assistant_is, pass it in the retrieved context.
        """
        return self.assistant_id
