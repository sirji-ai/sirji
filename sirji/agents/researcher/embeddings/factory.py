from .openai_assistant import OpenAIAssistantEmbeddings
from tools.logger import researcher as logger

class EmbeddingsFactory:
    @classmethod
    def get_instance(cls, embeddings_type):
        logger.info(f"Researcher: Getting instance for {embeddings_type}")

        if embeddings_type == "openai_assistant":
            return OpenAIAssistantEmbeddings()
        else:
            raise ValueError(
                "Unsupported embeddings_type. Please provide a valid embeddings_type.")

# Example usage:
# embeddings = EmbeddingsFactory.get_instance("openai_assistant")
