from abc import ABC, abstractmethod


class BaseEmbeddings(ABC):

    @abstractmethod
    def index(self, folder_path):
        """
        Index files in the specified folder.
        """
        pass

    @abstractmethod
    def retrieve_context(self, problem_statement):
        """
        Retrieve context using embeddings match for a problem statement. 
        """
        pass
