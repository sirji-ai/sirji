from .openai_assistant import OpenAIAssistantInferer
from tools.logger import researcher as logger

class InfererFactory:
    @classmethod
    def get_instance(cls, inferer_type):
        logger.info(f"Researcher: Getting instance for {inferer_type}")
        
        if inferer_type == "openai_assistant":
            return OpenAIAssistantInferer()
        else:
            raise ValueError(
                "Unsupported embeddings_type. Please provide a valid embeddings_type.")

# Example usage:
# embeddings = InfererFactory.get_instance("openai_assistant")
