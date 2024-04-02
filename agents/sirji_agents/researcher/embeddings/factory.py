from .openai_assistant import OpenAIAssistantEmbeddings


class EmbeddingsFactory:
    @classmethod
    def get_instance(cls, embeddings_type, init_payload):
        if embeddings_type == "openai_assistant":
            return OpenAIAssistantEmbeddings(init_payload)
        else:
            raise ValueError("Unsupported embeddings_type.")
