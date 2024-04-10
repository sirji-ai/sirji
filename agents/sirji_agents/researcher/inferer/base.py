from abc import ABC, abstractmethod


class ResearcherInfererBase(ABC):

    @abstractmethod
    def generate_prompt(self, retrieved_context, problem_statement):
        """
        Generates a prompt that combines the problem statement and the retrieved context.

        :param retrieved_context: The context information retrieved based on embeddings match.
        :param problem_statement: The initial problem statement or query.
        :return: A prompt string that combines both the problem statement and the retrieved context.
        """
        pass

    @abstractmethod
    def infer(self, retrieved_context, problem_statement):
        """
        Infers an answer by calling a chat model using the retrieved context and the problem statement.

        :param retrieved_context: The context information retrieved based on embeddings match.
        :param problem_statement: The initial problem statement or query.
        :return: The model's response based on the combined information of the problem statement and the retrieved context.
        """
        pass
