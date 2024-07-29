from sirji_tools.logger import create_logger
from sirji_messages import message_parse, ActionEnum, AgentEnum, allowed_response_templates, permissions_dict, ActionEnum,  MessageIncorrectFormatError, MessageMultipleActionError, MessageUnRecognizedActionError, MessageMissingPropertyError, MessageLengthConstraintError
from ..model_providers.factory import LLMProviderFactory
from .system_prompts.factory import SystemPromptsFactory
from ...decorators import retry_on_exception

class GenericAgentInfer():
    def __init__(self, config, agent_output_folder_index, file_summaries=None):
        # Initialize the logger as an instance variable
        self.logger = create_logger(f"{config['id']}.log", 'debug')
  
        self.logger.info(config)
        self.logger.info(agent_output_folder_index)
        
        self.config = config
        self.agent_output_folder_index = agent_output_folder_index
        self.file_summaries = file_summaries

    def message(self, input_message, history=[]):
        conversation = self.__prepare_conversation(input_message, history)

        self.logger.info(f"Incoming: \n{input_message}")
        self.logger.info("Calling OpenAI Chat Completions API\n")

        response_message, prompt_tokens, completion_tokens = self.__get_response(conversation)

        return response_message, conversation, prompt_tokens, completion_tokens

    def __prepare_conversation(self, input_message, history):
        conversation = []

        if not history:
            conversation.append(
                {"role": "system", "content": SystemPromptsFactory.get_system_prompt(self.config, self.agent_output_folder_index)})
        else:
            if history[0]['role'] == "system":
                history[0]['content'] = SystemPromptsFactory.get_system_prompt(self.config, self.agent_output_folder_index)
            conversation = history
        
        parsed_input_message = message_parse(input_message)
        conversation.append({"role": "user", "content": input_message, "parsed_content": parsed_input_message})
        
        return conversation

    def __get_response(self, conversation):
        retry_llm_count = 0
        response_message = ''
        prompt_tokens = 0
        completion_tokens = 0

        while(True):
            response_message, current_prompt_tokens, current_completion_tokens = self.__call_llm(conversation)
            
            prompt_tokens += current_prompt_tokens
            completion_tokens += current_completion_tokens
            try:
                # Attempt parsing
                parsed_response_message = message_parse(response_message)
                conversation.append({"role": "assistant", "content": response_message, "parsed_content": parsed_response_message})
                break
            except (MessageIncorrectFormatError, MessageMultipleActionError, MessageUnRecognizedActionError, MessageMissingPropertyError, MessageLengthConstraintError ) as e:
                if isinstance(e, MessageIncorrectFormatError):
                    self.logger.info("Error while parsing the message.\n")
                    retry_llm_count += 1
                    if retry_llm_count > 2:
                        raise e
                    self.logger.info(f"Requesting LLM to resend the message in correct format.\n")
                    conversation.append({"role": "assistant", "content": response_message, "parsed_content": {}})
                    conversation.append({"role": "user", "content": "Error obtained in processing your last response. Your response must conform strictly to one of the allowed Response Templates, as it will be processed programmatically and only these templates are recognized. Your response must be enclosed within '***' at the beginning and end, without any additional text above or below these markers. Not conforming above rules will lead to response processing errors."})
                if isinstance(e, MessageMissingPropertyError):
                    conversation.append({"role": "assistant", "content": response_message, "parsed_content": {}})
                    conversation.append({"role": "user", "content": "Error obtained in processing your last response. your response is missing some required properties. Please refer to the allowed response templates and provide the missing properties."})
                if isinstance(e, MessageUnRecognizedActionError):
                    conversation.append({"role": "assistant", "content": response_message, "parsed_content": {}})
                    conversation.append({"role": "user", "content": "Error obtained in processing your last response. Your response contains an unrecognized action. Please refer to the allowed response templates and provide a valid action."})
                if isinstance(e, MessageLengthConstraintError):
                    conversation.append({"role": "assistant", "content": response_message, "parsed_content": {}})
                    conversation.append({"role": "user", "content": "Error obtained in processing your last response. Your response does not have all the required properties."})
                if isinstance(e, MessageMultipleActionError):
                    conversation.append({"role": "assistant", "content": response_message, "parsed_content": {}})
                    conversation.append({"role": "user", "content": "Error obtained in processing your last response. Your response contains more than one ACTION keyword."})
            except Exception as e:
                self.logger.info(f"Generic error while parsing message. Error: {e}\n")
                raise e
                        
        return response_message, prompt_tokens, completion_tokens
    
    @retry_on_exception()
    def __call_llm(self, conversation):
        history = []

        for message in conversation:
            history.append({"role": message['role'], "content": message['content']})

        model_provider = LLMProviderFactory.get_instance()

        return model_provider.get_response(history, self.logger)