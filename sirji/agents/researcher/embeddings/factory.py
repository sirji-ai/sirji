from .openai_assistant import OpenAIAssistantEmbeddings


class EmbeddingsFactory:
    @classmethod
    def get_instance(cls, embeddings_type):
        if embeddings_type == "openai_assistant":
            return OpenAIAssistantEmbeddings()
        else:
            raise ValueError(
                "Unsupported embeddings_type. Please provide a valid embeddings_type.")

# Example usage:
# embeddings = EmbeddingsFactory.get_instance("openai_assistant")
