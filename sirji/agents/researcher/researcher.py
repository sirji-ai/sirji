import os

from .embeddings.factory import EmbeddingsFactory
from .inferer.factory import InfererFactory
from sirji.tools.crawler import crawl_urls


class Researcher:
    def __init__(self, embeddings_type, inferer_type):
        # Initialize the embeddings manager
        self.embeddings_manager = EmbeddingsFactory.get_instance(
            embeddings_type)

        # Initialize the inferer
        self.inferer = InfererFactory.get_instance(inferer_type)

    def index(self, urls):
        research_folder = 'workspace/researcher'
        crawl_urls(urls, research_folder)

        # Recursively walk through all folders and subfolders
        for root, dirs, files in os.walk(research_folder):
            for folder in dirs:
                folder_path = os.path.join(root, folder)
                print(folder_path)
                
                # Call embeddings_manager.index on each folder
                response = self.embeddings_manager.index(folder_path)
                # Optional: You may want to do something with the response

    def infer(self, problem_statement):
        retrieved_context = self.embeddings_manager.retrieve_context(
            problem_statement)

        return self.inferer.infer(retrieved_context, problem_statement)
