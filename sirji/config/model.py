import os

from openai import OpenAI


class ModelClient:
    def __init__(self):
        try:
            # Fetch OpenAI API key from environment variable
            api_key = os.environ.get("SIRJI_OPENAI_API_KEY")
            # Fetch boolean Ollama usage from environment variable
            usingOllama = os.environ.get("SIRJI_USE_OLLAMA", "False").lower() in [
                "true",
                "1",
                "yes",
            ]
            if usingOllama:
                ollama_model = os.environ.get(
                    "SIRJI_OLLAMA_MODEL", "deepseek-coder:latest"
                )
                self.client = OpenAI(
                    api_key="FOSS_FTW",
                    base_url="http://localhost:11434/v1",
                )
                self.model = ollama_model
            else:
                self.client = OpenAI(api_key=api_key)
                self.model = "model"
        except Exception as e:
            print(e)
            raise ValueError(
                "OpenAI API key or Ollama usage is not set as an environment variable in .env."
            )
