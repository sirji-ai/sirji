from .openai_assistant import OpenAIAssistantInferer


class InfererFactory:
    @classmethod
    def get_instance(cls, inferer_type, init_payload):
        if inferer_type == "openai_assistant":
            return OpenAIAssistantInferer(init_payload)
        else:
            raise ValueError("Unsupported inferer_type.")
