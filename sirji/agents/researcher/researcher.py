import os

from .embeddings.factory import EmbeddingsFactory
from .inferer.factory import InfererFactory
from sirji.tools.crawler import crawl_urls
from sirji.tools.search import search_for
from sirji.tools.logger import researcher as logger


class Researcher:
    def __init__(self, embeddings_type, inferer_type):
        logger.info("Researcher: Initializing...")

        # Initialize the embeddings manager
        self.embeddings_manager = EmbeddingsFactory.get_instance(
            embeddings_type)

        # Initialize the inferer
        self.inferer = InfererFactory.get_instance(inferer_type)

        self.research_folder = 'workspace/researcher'

        logger.info("Researcher: Completed initializing")

    def index(self, urls):
        logger.info("Researcher: Started indexing the URLs")
        crawl_urls(urls, self.research_folder)
        self._reindex()
        logger.info("Researcher: Completed indexing the URLs")

    def search_and_index(self, query):
        logger.info("Researcher: Started searching for the query")
        urls = search_for(query)
        self.index(urls)

    def infer(self, problem_statement):
        retrieved_context = self.embeddings_manager.retrieve_context(
            problem_statement)

        return self.inferer.infer(retrieved_context, problem_statement)

    def _reindex(self):
        logger.info("Researcher: Recursively indexing the research folder")

        # Recursively walk through all folders and sub-folders
        for root, dirs, files in os.walk(self.research_folder):
            for folder in dirs:
                folder_path = os.path.join(root, folder)
                print(folder_path)

                # Call embeddings_manager.index on each folder
                response = self.embeddings_manager.index(folder_path)
                # Optional: You may want to do something with the response

        logger.info(
            "Researcher: Completed recursively indexing the research folder")
