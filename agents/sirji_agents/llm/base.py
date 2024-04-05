from openai import OpenAI
import os

from sirji_messages import AgentSystemPromptFactory, message_parse, MessageParsingError


class SingletonMeta(type):
    """Singleton Meta Class for ensuring one instance creation."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class LLMAgentBase(metaclass=SingletonMeta):
    def __init__(self, agent_enum, logger):
        api_key = os.environ.get("SIRJI_OPENAI_API_KEY")
        if api_key is None:
            raise ValueError(
                "OpenAI API key is not set as an environment variable")

        self.client = OpenAI(api_key=api_key)
        self.agent_enum = agent_enum
        self.logger = logger

    def message(self, input_message, history=[]):
        conversation = self.__prepare_conversation(input_message, history)

        self.logger.info(f"Incoming: \n{input_message}")
        self.logger.info("Calling OpenAI Chat Completions API\n")

        response_message = self.__get_response(conversation)

        return response_message, conversation

    def __prepare_conversation(self, input_message, history):
        conversation = []

        if not history:
            prompt_class = AgentSystemPromptFactory[self.agent_enum.name]
            conversation.append(
                {"role": "system", "content": prompt_class().system_prompt()})
        else:
            conversation = history

        parsed_input_message = message_parse(input_message)
        conversation.append({"role": "user", "content": input_message, "parsed_content": parsed_input_message})

        return conversation

    def __get_response(self, conversation):
        
        retry_llm_count = 0
        response_message = ''

        while(True):
            response_message = self.__call_llm(conversation)
            try:
                # Attempt parsing
                parsed_response_message = message_parse(response_message)
                conversation.append({"role": "assistant", "content": response_message, "parsed_content": parsed_response_message})
                break
            except MessageParsingError as e:
                self.logger.info("Error while parsing the message.\n")
                retry_llm_count += 1
                if retry_llm_count > 2:
                    raise e
                self.logger.info(f"Requesting LLM to resend the message in correct format.\n")
                conversation.append({"role": "assistant", "content": response_message, "parsed_content": {}})
                conversation.append({"role": "user", "content": "The last message was not as per the allowed message formats. Please resend it with proper formatting."})
            except Exception as e:
                self.logger.info(f"Generic error while parsing message. Error: {e}\n")
                raise e
            
            
        return response_message
    
    def __call_llm(self, conversation):
        history = []

        for message in conversation:
            history.append({"role": message['role'], "content": message['content']})

        chat_completion = self.client.chat.completions.create(
            messages=history,
            model="gpt-4-turbo-preview",
            temperature=0,
            max_tokens=4095,
        )

        response_message = chat_completion.choices[0].message.content

        self.logger.info(f"Raw response from Chat Completions API: \n{response_message}\n\n\n")

        return response_message
