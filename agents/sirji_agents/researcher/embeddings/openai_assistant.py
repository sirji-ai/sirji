import os
import json
import hashlib
from openai import OpenAI

from sirji_tools.logger import create_logger

from .base import BaseEmbeddings

BATCH_SIZE = 10
MAX_RETRIES = 2

class OpenAIAssistantEmbeddings(BaseEmbeddings):

    def __init__(self, init_payload={}):
        self.logger = create_logger("researcher.log", "debug")
        print("Initializing OpenAI Assistant Embeddings")
        self.logger.info("Initializing OpenAI Assistant Embeddings")
        self.uploaded_files_info = []

        # Fetch OpenAI API key from environment variable
        api_key = os.environ.get("SIRJI_MODEL_PROVIDER_API_KEY")

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

    def index(self, absolute_path, file_path):
        self.logger.info(f"Indexing files in the folder: {file_path}")

        # print(f"Indexing files in the folder: {file_path}")

        # hash_object = hashlib.md5(file_path.encode())
        # file_hash = hash_object.hexdigest()
        # target_file_name = f"{file_hash}.md"
        # """
        # Index files in the specified folder.
        # """

        # print(target_file_name)

        # print(' os.path.isfile(file_path)', os.path.isfile(absolute_path))
        # # Check if file is not already indexed
        # if os.path.isfile(absolute_path) and not any(d['local_path'] == file_path for d in self.index_data):
        #     print('in if')
        #     language_name = self._detect_language_from_extension(file_path)
        #     print('language_name', language_name)

        #     with open(absolute_path, 'r') as file_to_upload:
        #         content = file_to_upload.read()
                
        #     formatted_content = self._format_file_content(file_path, content, language_name)
        #     print('formatted_content', formatted_content)
            
        #     self.file_streams.append((target_file_name, formatted_content))

        self.logger.info(f"Completed indexing files in the folder: {file_path}")
    
    def upload_batches(self, file_streams):
        total_files = len(file_streams)

        for i in range(0, total_files, BATCH_SIZE):
            batch = file_streams[i:i + BATCH_SIZE]
            retry_count = 0

            while retry_count <= MAX_RETRIES:
                try:
                    uploaded_files = self._upload_file(batch)

                    list_batches_files = self._list_uploaded_files(uploaded_files.id)

                    # Collect file ID info for each uploaded file
                    for uploaded_file in list_batches_files.data:
                        file_info = {
                            'file_id': uploaded_file.id,
                            'created_at': uploaded_file.created_at,
                            'status': uploaded_file.status,
                        }

                        vector_store_file = self.client.files.retrieve(uploaded_file.id)

                        file_info['file_name'] = vector_store_file.filename

                        self.uploaded_files_info.append(file_info)

                        print("assistant_id", self.init_payload['assistant_id'])
                
                    self.logger.info(f"Successfully uploaded batch {i//BATCH_SIZE + 1} of {total_files//BATCH_SIZE + 1}")
                    break
                except Exception as e:
                    print(f"Failed to upload batch {i//BATCH_SIZE + 1} of {total_files//BATCH_SIZE + 1}, attempt {retry_count + 1}: {e}")
                    self.logger.error(f"Failed to upload batch {i//BATCH_SIZE + 1} of {total_files//BATCH_SIZE + 1}, attempt {retry_count + 1}: {e}")
                    retry_count += 1
                    if retry_count > MAX_RETRIES:
                        self.logger.error(f"Giving up on batch {i//BATCH_SIZE + 1} after {MAX_RETRIES + 1} attempts")

        print("self.uploaded_files_info", self.uploaded_files_info)

        return self.uploaded_files_info

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
        
    def _list_uploaded_files(self, batch_id):
        self.logger.info("Listing uploaded files")
        return self.client.beta.vector_stores.file_batches.list_files(
            vector_store_id= self.init_payload['vector_store_id'],
            batch_id=batch_id
        )

    def _upload_file(self, batch):
        self.logger.info(f"Uploading file to OpenAI")
       
        """
        Upload file content to OpenAI.
        """
        return self.client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id= self.init_payload['vector_store_id'],
        files=batch
        )

    def _associate_file(self, file_id):
        self.logger.info(f"Associating {file_id} file with assistant")
        """
        Associate file with assistant.
        """
        return self.client.beta.assistants.files.create(
               assistant_id=self.init_payload['assistant_id'], file_id=file_id)
    
    def delete_file_from_vector_store(self, file_id):
        self.logger.info(f"Deleting {file_id} file from vector store")
        """
        Delete file from vector store.
        """
        self.client.beta.vector_stores.files.delete(
                vector_store_id= self.init_payload['vector_store_id'], file_id=file_id
            )
       
        print("res delete_file_from_vector_store")

    
    def delete_file_from_assistant(self, file_id):
        self.logger.info(f"Deleting {file_id} file")
        """
        Delete file.
        """
        self.client.files.delete(file_id)

        print("res delete_file_from_assistant")
    


