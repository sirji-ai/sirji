from .base import LLMProviderBase
from openai import OpenAI

class DeepSeekProvider(LLMProviderBase):
    def __init__(self, api_key, model):
        super().__init__(api_key, model)

    def get_response(self, messages, logger):
        client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")

        chat_completion = client.chat.completions.create(
            messages=messages,
            model=self.model,
            temperature=0,
            max_tokens=4095,
        )

        response_message = chat_completion.choices[0].message.content

        # Get the total tokens used in the response
        prompt_tokens = chat_completion.usage.prompt_tokens
        completion_tokens = chat_completion.usage.completion_tokens
        
        logger.info(f"Raw response from Chat Completions API: \n{response_message}\n\n\n")

        return response_message, prompt_tokens, completion_tokens