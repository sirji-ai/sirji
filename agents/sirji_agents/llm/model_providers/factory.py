import os
from .base import LLMProviderBase
from .openai import OpenAIProvider

class LLMProviderFactory:
    @staticmethod
    def get_instance():
        # Reading from environment variables and setting defaults.
        provider_name = os.environ.get('SIRJI_MODEL_PROVIDER', 'openai').lower()
        model = os.environ.get('SIRJI_MODEL', 'gpt-4o')
        api_key = os.environ.get('SIRJI_MODEL_PROVIDER_API_KEY', os.environ.get('SIRJI_OPENAI_API_KEY'))

        if not api_key:
            raise EnvironmentError("SIRJI_MODEL_PROVIDER_API_KEY is not set in environment variables.")
        
        if provider_name == 'openai':
            print('Model used:', model)
            return OpenAIProvider(api_key, model)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_name}")