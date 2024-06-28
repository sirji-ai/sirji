from .openai_assistant import OpenAIAssistantInferer
import os


class InfererFactory:
    @classmethod
    def get_instance(cls, init_payload):

        provider_name = os.environ.get('SIRJI_MODEL_PROVIDER').lower()
      
        if provider_name == "openai":
            return OpenAIAssistantInferer(init_payload)
        else:
            raise ValueError("Unsupported inferer_type.")
