from .embeddings.factory import EmbeddingsFactory
from .inferer.factory import InfererFactory  # Corrected from your instructions
from sirji.crawler import crawl_urls


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

        self.embeddings_manager.index(research_folder)
