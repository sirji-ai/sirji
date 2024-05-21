import textwrap
import os
import json

# TODO - log file should be dynamically created based on agent ID
from sirji_tools.logger import p_logger as logger

from sirji_messages import message_parse, MessageParsingError, MessageValidationError, ActionEnum, AgentEnum, allowed_response_templates, permissions_dict
from .model_providers.factory import LLMProviderFactory

class Orchestrator():
    def __init__(self, agent_output_folder_index):
        self.agent_output_folder_index = agent_output_folder_index

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
            if history[0]['role'] == "system":
                history[0]['content'] = self.system_prompt()
                
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
        
        pseudo_code = textwrap.dedent(f"""
            Pseudo code which you must follow:
                1. INVOKE_AGENT REQUIREMENT_GATHERER to QUESTION SIRJI_USER to provide the problem statement and then store it in Agent Output folder.
                2. INVOKE_AGENT RECIPE_SELECTOR to Get the recipe selected from the available recipes by SIRJI_USER and then store it in Agent Output Folder.
                3. READ_AGENT_OUTPUT_FILES the selected recipe from the Agent Output Folder using EXECUTOR.
                4. Proceed sequentially over the prescribed tasks in the recipe.
                    - For each task, invoke the agent specified in the recipe alongside the task, explaining the task in the BODY of the invocation.
            """)

        # instructions = textwrap.dedent(f"""
        #     Instructions:
        #     - Manage the task workflow by interpreting the "recipe", which outlines a series of prescribed tasks.
        #     - Proceed sequentially over the prescribed tasks.
        #     - For each task, invoke the agent specified in the recipe alongside the task, explaining the task in the BODY of the invocation.
        #     """)

        allowed_response_templates_str = textwrap.dedent(f"""
            Allowed Response Templates:""")
        
        allowed_response_templates_str += '\n' + allowed_response_templates(AgentEnum.ORCHESTRATOR, AgentEnum.SIRJI_USER, permissions_dict[(AgentEnum.ORCHESTRATOR, AgentEnum.SIRJI_USER)]) + '\n'
        allowed_response_templates_str += '\n' +  allowed_response_templates(AgentEnum.ORCHESTRATOR, AgentEnum.ANY, permissions_dict[(AgentEnum.ORCHESTRATOR, AgentEnum.ANY)]) + '\n'

        action_list = permissions_dict[(AgentEnum.ANY, AgentEnum.EXECUTOR)]
        allowed_response_templates_str += '\n' +  allowed_response_templates(AgentEnum.ANY, AgentEnum.EXECUTOR, action_list) + '\n'

        current_agent_output_index = f"Current contents of Agent Output Index:\n{json.dumps(self.agent_output_folder_index, indent=4)}"

        return f"{initial_intro}\n{pseudo_code}\n{allowed_response_templates_str}\n{current_agent_output_index}".strip()
