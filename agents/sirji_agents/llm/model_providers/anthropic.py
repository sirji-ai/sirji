from .base import LLMProviderBase
from anthropic import Anthropic

class AnthropicProvider(LLMProviderBase):
    def __init__(self, api_key, model):
        super().__init__(api_key, model)

    def get_response(self, messages, logger):
        client = Anthropic(
            api_key=self.api_key,
        )
        
        system = messages[0]['content']

        message = client.messages.create(
            system=system,
            messages=messages[1:],
            model=self.model,
            temperature=0,
            max_tokens=4095,
        )

        response_message = message.content[0].text

        # Get the total tokens used in the response
        prompt_tokens = message.usage.input_tokens
        completion_tokens = message.usage.output_tokens
        
        logger.info(f"Raw response from Chat Completions API: \n{response_message}\n\n\n")

        return response_message, prompt_tokens, completion_tokens