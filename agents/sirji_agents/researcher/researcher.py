import os

from sirji_tools.crawler import crawl_urls
from sirji_tools.search import search_for
from sirji_tools.logger import create_logger 

from sirji_messages import message_parse, MessageFactory, ActionEnum

from .embeddings.factory import EmbeddingsFactory
from .inferer.factory import InfererFactory


class ResearchAgent:
    def __init__(self, embeddings_type, inferer_type, init_payload={}):
        """Initialize Researcher with specific embeddings and inferer types."""
        self.logger = create_logger("researcher.log", "debug")
        self.logger.info("Initializing researcher...")

        self._embeddings_manager = EmbeddingsFactory.get_instance(
            embeddings_type, init_payload)

        self.init_payload = self._embeddings_manager.init_payload

        self._inferer = InfererFactory.get_instance(
            inferer_type, self.init_payload)

        self._research_folder = os.path.join(self._get_run_path(), "researcher")

        self.logger.info("Completed initializing researcher")

    def message(self, input_message):
        """Public method to process input messages and dispatch actions."""
        parsed_message = message_parse(input_message)
        action = parsed_message.get("ACTION")

        if action == ActionEnum.TRAIN_USING_SEARCH_TERM.name:
            return self._handle_train_using_search_term(parsed_message)
        elif action == ActionEnum.TRAIN_USING_URL.name:
            return self._handle_train_using_url(parsed_message)
        elif action == ActionEnum.INFER.name:
            return self._handle_infer(parsed_message)
        
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

    def _handle_train_using_search_term(self, parsed_message):
        """Private method to handle training using a search term."""
        self.logger.info(
            f"Training using search term: {parsed_message.get('TERM')}")
        self._search_and_index(parsed_message.get('TERM'))

        return self._generate_message(ActionEnum.TRAINING_OUTPUT, "Training using search term completed successfully"), 0, 0

    def _handle_train_using_url(self, parsed_message):
        """Private method to handle training using a specific URL."""
        self.logger.info(f"Training using URL: {parsed_message.get('URL')}")
        self._index([parsed_message.get('URL')])

        return self._generate_message(ActionEnum.TRAINING_OUTPUT, "Training using url completed successfully"), 0, 0

    def _handle_infer(self, parsed_message):
        """Private method to handle inference requests."""
        self.logger.info(f"Infering: {parsed_message.get('DETAILS')}")
        response, prompt_tokens, completion_tokens= self._infer(parsed_message.get('DETAILS'))

        return self._generate_message(ActionEnum.RESPONSE, response), prompt_tokens, completion_tokens

    def _generate_message(self, action_enum, details):
        """Generate standardized messages for responses based on action enum."""
        message_class = MessageFactory[action_enum.name]
        return message_class().generate({"details": details})

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
        retrieved_context = self._embeddings_manager.retrieve_context(
            problem_statement)
        return self._inferer.infer(retrieved_context, problem_statement)

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
