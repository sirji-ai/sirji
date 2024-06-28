from .openai_assistant import OpenAIAssistantEmbeddings
import os


class EmbeddingsFactory:
    @classmethod
    def get_instance(cls, init_payload):
    
        provider_name = os.environ.get('SIRJI_MODEL_PROVIDER').lower()

        if provider_name == "openai":
            return OpenAIAssistantEmbeddings(init_payload)
        else:
            raise ValueError("Unsupported embeddings_type.")
