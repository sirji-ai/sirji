import textwrap
import os

# TODO - log file should be dynamically created based on agent ID
from sirji_tools.logger import p_logger as logger

from sirji_messages import message_parse, MessageParsingError, MessageValidationError, ActionEnum, AgentEnum, allowed_response_templates
from .model_providers.factory import LLMProviderFactory

class Orchestrator():
    def __init__(self, recipe):
        
        self.recipe = recipe

    def message(self, input_message, history=[]):
        conversation = self.__prepare_conversation(input_message, history)

        logger.info(f"Incoming: \n{input_message}")
        logger.info("Calling OpenAI Chat Completions API\n")

        response_message, prompt_tokens, completion_tokens = self.__get_response(conversation)

        return response_message, conversation, prompt_tokens, completion_tokens

    def __prepare_conversation(self, input_message, history):
        conversation = []

        logger.info(history)

        if not history:
            conversation.append(
                {"role": "system", "content": self.system_prompt()})
        else:
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
            except (MessageParsingError, MessageValidationError) as e:
            # Handling both MessageParsingError and MessageValidationError similarly
                logger.info("Error while parsing the message.\n")
                retry_llm_count += 1
                if retry_llm_count > 2:
                    raise e
                logger.info(f"Requesting LLM to resend the message in correct format.\n")
                conversation.append({"role": "assistant", "content": response_message, "parsed_content": {}})
                conversation.append({"role": "user", "content": "Error obtained in processing your last response. Your response must conform strictly to one of the allowed Response Templates, as it will be processed programmatically and only these templates are recognized. Your response must be enclosed within '***' at the beginning and end, without any additional text above or below these markers. Not conforming above rules will lead to response processing errors."})
            except Exception as e:
                logger.info(f"Generic error while parsing message. Error: {e}\n")
                raise e
            
            
        return response_message, prompt_tokens, completion_tokens
    
    def __call_llm(self, conversation):
        history = []

        for message in conversation:
            history.append({"role": message['role'], "content": message['content']})

        model_provider = LLMProviderFactory.get_instance()

        return model_provider.get_response(history, logger)

    def system_prompt(self):
        initial_intro = textwrap.dedent(f"""
            You are an agent named "Orchestration Agent", a component of the Sirji AI agentic framework.
            Your Agent ID: ORCHESTRATOR
            Your OS (refered as SIRJI_OS later): {os.name}""")

        instructions = textwrap.dedent(f"""
            Instructions:
            - Manage the task workflow by interpreting the "recipe", which outlines a series of prescribed tasks.
            - Proceed sequentially over the prescribed tasks.
            - For each task, invoke the agent specified in the recipe alogside the task, explaining the task in the BODY of the invocation.
            """)

        formatted_recipe = self.__format_recipe()

        allowed_response_templates = textwrap.dedent(f"""
            Allowed Response Templates:""")
        
        allowed_response_templates += '\n' + allowed_response_templates(AgentEnum.ORCHESTRATOR, AgentEnum.SIRJI_USER) + '\n'
        allowed_response_templates += '\n' +  allowed_response_templates(AgentEnum.ORCHESTRATOR, AgentEnum.ANY) + '\n'

        return f"{initial_intro}\n{instructions}\n{formatted_recipe}{allowed_response_templates}".strip()
    def __format_recipe(self):
        formatted = "Recipe:\n"
        # Adding prescribed tasks with enumeration
        formatted += "- Prescribed tasks\n"
        for index, task in enumerate(self.recipe["prescribed_tasks"], start=1):
            formatted += f"   {index}. {task['task']}\n"
            formatted += f"      Agent to invoke: {task['agent']}\n"
        
        # Adding tips
        if "tips" in self.recipe and self.recipe["tips"]:
            formatted += "- Tips:\n"
            for tip in self.recipe["tips"]:
                formatted += f"   - {tip['tip']}\n"
                formatted += f"      Agent to invoke: {tip['agent']}\n"
        
        return formatted
