from .openai_assistant import OpenAIAssistantInferer


class EmbeddingsFactory:
    @classmethod
    def get_instance(cls, inferer_type):
        if inferer_type == "openai_assistant":
            return OpenAIAssistantInferer()
        else:
            raise ValueError(
                "Unsupported embeddings_type. Please provide a valid embeddings_type.")

# Example usage:
# embeddings = EmbeddingsFactory.get_instance("openai_assistant")
