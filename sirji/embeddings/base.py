from abc import ABC, abstractmethod


class BaseEmbeddings(ABC):

    @abstractmethod
    def index(self, folder_path):
        """
        Index files in the specified folder.
        """
        pass
