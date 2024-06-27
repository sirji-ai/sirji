import os
import json
import hashlib
from openai import OpenAI

from sirji_tools.logger import create_logger

from .base import BaseEmbeddings

class OpenAIAssistantEmbeddings(BaseEmbeddings):

    def __init__(self, init_payload={}):
        self.logger = create_logger("researcher.log", "debug")
        self.logger.info("Initializing OpenAI Assistant Embeddings")

        # Fetch OpenAI API key from environment variable
        api_key = os.environ.get("SIRJI_OPENAI_API_KEY")

        if api_key is None:
            raise ValueError(
                "OpenAI API key is not set as an environment variable")

        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)

        # Existing initialization logic
        self.init_payload = init_payload

        # Ensure assistant_id is provided in init_payload
        if 'assistant_id' not in self.init_payload:
            raise ValueError("assistant_id must be provided in init_payload")

        self.index_file_path = os.path.join(self._get_run_path(), 'researcher', 'file_index.json')

        # Load or initialize the index file
        self.index_data = self._load_or_initialize_index_file()

        self.logger.info("Completed initializing OpenAI Assistant Embeddings")

    def index(self, folder_path):
        self.logger.info(f"Indexing files in the folder: {folder_path}")

        """
        Index files in the specified folder.
        """
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Check if file is not already indexed
            if os.path.isfile(file_path) and not any(d['local_path'] == file_path for d in self.index_data):
                language_name = self._detect_language_from_extension(filename)

                with open(file_path, 'r') as file_to_upload:
                    content = file_to_upload.read()
                    
                formatted_content = self._format_file_content(file_path, content, language_name)
                
                response = self._upload_file(formatted_content, filename)
                if response['status'] == 'processed':
                    file_id = response['id']
                    # Associate file with assistant
                    associate_response = self._associate_file(file_id)
                    if not associate_response['id']:
                        self.logger.error(
                            f"Failed to associate file {filename} with assistant.")
                        continue
                    self.index_data.append(
                        {'local_path': file_path, 'file_id': file_id})
                    self._update_index_file()
                else:
                    self.logger.error(
                        f"Failed to upload file {filename}. Status Code: {response.get('status_code')}")

        self.logger.info(f"Completed indexing files in the folder: {folder_path}")

    def retrieve_context(self, problem_statement):
        """
        Retrieve context using embeddings match for a problem statement.
        For OpenAI Assistants API, this step is not needed.
        To re-use the assistant_id, pass it in the retrieved context.
        """
        return ""

    def _get_project_folder(self):
        project_folder = os.environ.get("SIRJI_PORJECT")
        if project_folder is None:
            raise ValueError(
                "SIRJI_PORJECT is not set as an environment variable")
        return project_folder

    def _get_run_path(self):
        run_id = os.environ.get("SIRJI_RUN_PATH")
        if run_id is None:
            raise ValueError(
                "SIRJI_RUN_PATH is not set as an environment variable")
        return run_id
    
    def _load_or_initialize_index_file(self):
        self.logger.info("Initializing the index file")
        """
        Load or initialize the index file.
        """
        if os.path.exists(self.index_file_path):
            with open(self.index_file_path, 'r') as index_file:
                return json.load(index_file)
        else:
            return []

    def _update_index_file(self):
        self.logger.info("Updating the index file with current index data")
        """
        Update the index file with current index data.
        """
        with open(self.index_file_path, 'w') as index_file:
            json.dump(self.index_data, index_file, indent=4)

    def _upload_file(self, content, original_filename):
        self.logger.info(f"Uploading file to OpenAI: {original_filename}")
        """
        Upload file content to OpenAI.
        """
        return self.client.files.create(
            file=(original_filename, content),
            purpose='assistants'
        )

    def _associate_file(self, file_id):
        self.logger.info(f"Associating {file_id} file with assistant")
        """
        Associate file with assistant.
        """
        return self.client.beta.assistants.files.create(
               assistant_id=self.init_payload['assistant_id'], file_id=file_id)

    def _detect_language_from_extension(self, filename):
        """
        Detect the programming language based on file extension.
        """
        extension_to_language = {
            '.py': 'python',
            '.js': 'javascript',
            '.rb': 'ruby',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.cs': 'csharp',
            '.php': 'php',
            '.html': 'html',
            '.css': 'css',
            '.go': 'go',
            '.swift': 'swift',
            '.rs': 'rust',
            '.ts': 'typescript',
        }
        _, ext = os.path.splitext(filename)
        language = extension_to_language.get(ext, 'plain text')
        self.logger.info(f"Detected language {language} for {filename}")
        return language

    def _format_file_content(self, file_path, content, language_name):
        """
        Format the file content along with metadata.
        """
        return (
            f"File path: {file_path}\n\n"
            f"File content:\n"
            f"```{language_name}\n"
            f"{content}\n"
            f"```"
        )
