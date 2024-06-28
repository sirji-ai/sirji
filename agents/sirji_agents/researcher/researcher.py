import os
import json
import textwrap
from openai import OpenAI
import hashlib


from sirji_tools.crawler import crawl_urls
from sirji_tools.search import search_for
from sirji_tools.logger import create_logger 
from sirji_messages import message_parse, MessageFactory, ActionEnum

from .embeddings.factory import EmbeddingsFactory
from .inferer.factory import InfererFactory


DEFAULT_SKIP_LIST = [
    '__pycache__',
    '.git',
    '.github',
    '.gitlab',
    '.vscode',
    '.idea',
    'node_modules',
    '.DS_Store',
    'venv',
    '.venv',
    '.sass-cache',
    'dist',
    'out',
    'build',
    'logs',
    '.npm',
    'temp',
    'tmp',
    '.env',
    '.env.test',
    '.env.local',
    '.env.development',
    '.env.production',
    '.env.staging'
]


class ResearchAgent:
    def __init__(self, init_payload={}):
        """Initialize Researcher with specific embeddings and inferer types."""
        self.logger = create_logger("researcher.log", "debug")
        self.logger.info("Initializing researcher...")

        self.init_payload = init_payload

        self._research_folder = os.path.join(self._get_run_path(), "researcher")

        self.logger.info("Completed initializing researcher")

        # Initialize SKIP_LIST
        self.skip_list = set(DEFAULT_SKIP_LIST)

    def message(self, input_message):
        """Public method to process input messages and dispatch actions."""
        parsed_message = message_parse(input_message)
        action = parsed_message.get("ACTION")

        if action == ActionEnum.CREATE_ASSISTANT.name:
            return self._handle_create_assistant(parsed_message), 0, 0
        else:
            if 'assistant_id' not in self.init_payload:
                error_response = "Error: Active assistant_id not found. Please create an assistant first."
                return self._generate_message(parsed_message.get('TO'), parsed_message.get('FROM'), error_response), 0, 0

            self._embeddings_manager = EmbeddingsFactory.get_instance(self.init_payload)
            
            if action == ActionEnum.SYNC_CODEBASE.name:
                return self._sync_codebase(parsed_message), 0, 0
            elif action == ActionEnum.INFER.name:
                return self._handle_infer(parsed_message)

            # if action == ActionEnum.TRAIN_USING_SEARCH_TERM.name:
            #     return self._handle_train_using_search_term(parsed_message)
            # elif action == ActionEnum.TRAIN_USING_URL.name:
            #     return self._handle_train_using_url(parsed_message)
           
        
    def _get_project_folder(self):
        project_folder = os.environ.get("SIRJI_PROJECT")
        if project_folder is None:
            raise ValueError(
                "SIRJI_PROJECT is not set as an environment variable")
        return project_folder
    
    def _get_run_path(self):
        run_path = os.environ.get("SIRJI_RUN_PATH")
        if run_path is None:
            raise ValueError(
                "SIRJI_RUN_PATH is not set as an environment variable")
        return run_path

    # def _handle_train_using_search_term(self, parsed_message):
    #     """Private method to handle training using a search term."""
    #     self.logger.info(
    #         f"Training using search term: {parsed_message.get('TERM')}")
    #     self._search_and_index(parsed_message.get('TERM'))

    #     return self._generate_message(ActionEnum.TRAINING_OUTPUT, "Training using search term completed successfully"), 0, 0

    # def _handle_train_using_url(self, parsed_message):
    #     """Private method to handle training using a specific URL."""
    #     self.logger.info(f"Training using URL: {parsed_message.get('URL')}")
    #     self._index([parsed_message.get('URL')])

    #     return self._generate_message(ActionEnum.TRAINING_OUTPUT, "Training using url completed successfully"), 0, 0

    def _handle_infer(self, parsed_message):
        """Private method to handle inference requests."""
        self.logger.info(f"Infering: {parsed_message.get('BODY')}")
        response, prompt_tokens, completion_tokens = self._infer(parsed_message.get('BODY'))

        print(f"Response: {response}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Completion tokens: {completion_tokens}")

        return self._generate_message(parsed_message.get('TO'), parsed_message.get('FROM'), response), prompt_tokens, completion_tokens

    def _handle_create_assistant(self, parsed_message):
        """Private method to handle assistant creation requests."""
        self.logger.info("Creating assistant")
        self.create_assistant(parsed_message.get('BODY'))    
        response = "Assistant created successfully"
    
        return self._generate_message(parsed_message.get('TO'), parsed_message.get('FROM'), response) 

    def _generate_message(self, from_agent_id, to_agent_id, contents):
        """Generate standardized messages for responses based on action enum."""
        message_class = MessageFactory[ActionEnum.RESPONSE.name]
        message_str = message_class().generate({
        "from_agent_id": f"{from_agent_id}",
        "to_agent_id": f"{to_agent_id}",
        "step": "EMPTY",
        "summary": "EMPTY",
        "body": textwrap.dedent(f"""
        {contents}
        """)})

        return message_str

    def _index(self, urls):
        """Index given URLs."""
        self.logger.info("Started indexing the URLs")
        crawl_urls(urls, self._research_folder)
        self.__reindex()
        self.logger.info("Completed indexing the URLs")

    def _search_and_index(self, query):
        """Search for a query and index resulting URLs."""
        urls = search_for(query)
        self._index(urls)

    def _infer(self, problem_statement):
        """Infer based on the given problem statement and context."""

        self._inferer = InfererFactory.get_instance(self.init_payload)
        
        return self._inferer.infer(problem_statement)

    def __reindex(self):
        """Re-index the research folder recursively. Note: This is treated exceptionally private."""
        self.logger.info("Recursively indexing the research folder")
        for root, dirs, files in os.walk(self._research_folder):
            for folder in dirs:
                folder_path = os.path.join(root, folder)
                # Improved logging
                self.logger.info(f"Indexing folder: {folder_path}")

                response = self._embeddings_manager.index(folder_path)
                # Optionally handle the response
        self.logger.info("Completed recursive indexing of the research folder")

    def _sync_codebase(self, parsed_message):
        """Sync codebase by reading .gitignore and indexing files."""
        try:
            project_root_path = self._get_project_folder()
            self.logger.info(f"Starting sync for project: {project_root_path}")
            self._read_gitignore(project_root_path)
            self._read_directory(project_root_path)
            self.logger.info("Completed syncing codebase")
            contents = "Sync codebase completed successfully"
            return self._generate_message(parsed_message.get('TO'), parsed_message.get('FROM'), contents)
        except Exception as e:
            self.logger.error(f"Error syncing codebase: {e}")
            contents = f"Error syncing codebase: {e}"
            return  self._generate_message(parsed_message.get('TO'), parsed_message.get('FROM'), contents)

    def _read_gitignore(self, project_root_path):
        """Read .gitignore file and update the skip_list."""
        print(f"Reading .gitignore file from {project_root_path}")
        try:
            gitignore_path = os.path.join(project_root_path, '.gitignore')
            with open(gitignore_path, 'r') as gitignore_file:
                entries = gitignore_file.readlines()
                new_entries = [
                    entry.strip() for entry in entries if entry.strip() and not entry.startswith('#')
                ]
                self.skip_list.update(new_entries)
                self.logger.info(f"Updated SKIP_LIST from .gitignore: {self.skip_list}")
        except FileNotFoundError:
            self.logger.warning(f".gitignore file not found in {project_root_path}")
        except Exception as e:
            self.logger.error(f"Error reading .gitignore: {e}")

    def _should_skip(self, name):
        """Check if the file or directory should be skipped."""
        return any(skip_item in name for skip_item in self.skip_list)

    def _read_directory(self, project_root_path):
        """Read directory and index files."""
        print(f"Reading directory: {project_root_path}")
        for root, dirs, files in os.walk(project_root_path):
            # Remove dirs that should be skipped
            dirs[:] = [d for d in dirs if not self._should_skip(d)]
            for file in files:
                if not self._should_skip(file):
                    file_path = os.path.join(root, file)
                    print(f"Indexing file: {file_path}")
                    self._index_file(file_path, project_root_path)

    def _index_file(self, file_path, project_root_path):
        """Index the individual file."""
        print(f"Indexing file: {file_path}")
        relative_file_path = os.path.relpath(file_path, project_root_path)
        print(f"Relative file path: {relative_file_path}")
        self._embeddings_manager.index(file_path, relative_file_path)
        
    def create_assistant(self, body):
        self.logger.info("Creating a new assistant instance")
        """
        Create a new assistant
        """

        api_key = os.environ.get("SIRJI_MODEL_PROVIDER_API_KEY")

        if api_key is None:
            raise ValueError(
                "OpenAI API key is not set as an environment variable")

        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)

        assistant = client.beta.assistants.create(
            name="Research Assistant",
            instructions=body,
            tools=[{"type": "file_search"}],
            model=os.environ.get("SIRJI_MODEL")
        )

        self.logger.info("Completed creating a new assistant")
        # Update payload
        self.logger.info(f"New assistant created with ID: {assistant.id}")

        run_id = os.environ.get("SIRJI_RUN_PATH")
        if run_id is not None:
         run_id = run_id.split("/")[-1]
     
        vector_store = client.beta.vector_stores.create(name=f"research-assistant-vector-store-{run_id}")

        assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        )

        # Store assistant details in a JSON file
        assistant_details = {
            "assistant_id": assistant.id,
            "vector_store_id": vector_store.id,
            "status": "created"
        }

        print(assistant_details)
        assistant_details_path = os.path.join(self._get_run_path(), "assistant_details.json")
        with open(assistant_details_path, 'w') as f:
            json.dump(assistant_details, f, indent=4)
