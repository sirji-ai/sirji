from .openai_cleanup import OpenAICleanup
import os


class CleanupFactory:
    @classmethod
    def get_instance(cls):

        provider_name = os.environ.get('SIRJI_MODEL_PROVIDER').lower()
      
        if provider_name == "openai":
            return OpenAICleanup()
        else:
            raise ValueError("Unsupported provider: {}".format(provider_name))
