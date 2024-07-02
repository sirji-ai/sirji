from abc import ABC, abstractmethod


class CleanupBase(ABC):

    @abstractmethod
    def delete_assistant(self, assistant_id):
        """
        Deletes the assistant.

        :param assistant_id: The assistant ID to be deleted.
        """
        pass

    @abstractmethod
    def delete_vector_store(self, vector_store_id):
        """
        Deletes the vector store.

        :param vector_store_id: The vector store ID to be deleted.
        """
        pass

    @abstractmethod
    def delete_file(self, file_path):
        """
        Deletes the file.

        :param file_path: The file path to be deleted.
        """
        pass
