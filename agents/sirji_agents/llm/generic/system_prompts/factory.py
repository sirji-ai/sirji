from .default import DefaultSystemPrompt
from .anthropic import AnthropicSystemPrompt
import os

class SystemPromptsFactory:
    @classmethod
    def get_system_prompt(cls, config, agent_output_folder_index):
    
        provider_name = os.environ.get('SIRJI_MODEL_PROVIDER').lower()

        if provider_name == "anthropic":
            return AnthropicSystemPrompt(config, agent_output_folder_index).system_prompt()
        else:
            return DefaultSystemPrompt(config, agent_output_folder_index).system_prompt()
