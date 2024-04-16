from abc import ABC, abstractmethod

class LLMProviderBase(ABC):
    @abstractmethod
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    def get_response(self, messages, logger):
        pass