import textwrap
import os
import json

# TODO - log file should be dynamically created based on agent ID
from sirji_tools.logger import o_logger as logger

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
                
        response_specifications = textwrap.dedent(f"""
            Your Response:
            - Your response must conform strictly to one of the allowed Response Templates, as it will be processed programmatically and only these templates are recognized.
            - Your response must be enclosed within '***' at the beginning and end, without any additional text above or below these markers.
            - Do not respond with two actions in the same response. Respond with one action at a time. Failing so will lead to response processing errors.                                                  
            - Not conforming above rules will lead to response processing errors.""")
        
        understanding_the_folders = textwrap.dedent("""
            Project Folder:
            - The Project Folder is your primary directory for accessing all user-specific project files, including code files, documentation, and other relevant resources.
            - When initializing Sirji, the SIRJI_USER selects this folder as the primary workspace for the project. You should refer to this folder exclusively for accessing and modifying project-specific files.
            
            Agent Output Folder:
            - The Agent Output Folder is designated for storing the results and data outputs generated by the agents (like you) of Sirji.
            - Ensure you do not confuse this folder with the Project Folder; remember, no project source files are stored here.
            - This folder is different from the project folder and this ensures that operational data is kept separate from project files.
            - Note: Always use STORE_IN_AGENT_OUTPUT and READ_AGENT_OUTPUT_FILES to write and read files to and from the Agent Output Folder.                                             
            
            Agent Output Index:
            - The Agent Output Index is an index file for the Agent Output Folder that keeps track of all files written by agents in that folder along with the a brief description of the file contents.
            - The Agent Output Index will look as follows:
              {
                  'agent_id/file_name': {
                        'description': 'description of the file contents'
                        'created_by': 'agent_id'
                  }
              }""")
        
        pseudo_code = textwrap.dedent(f"""
            Pseudo code which you must follow:
                1. Invoke agent RECIPE_SELECTOR to get the recipe selected from the available recipes by SIRJI_USER and then store it in Agent Output Folder.
                2. Read the selected recipe from the Agent Output Folder.
                3. Loop over the prescribed tasks in the selected recipe and invoke the agent specified in the recipe alongside the current task, explaining the task in the BODY of the invocation.
            """)

        allowed_response_templates_str = textwrap.dedent(f"""
            Allowed Response Templates:""")
        
        allowed_response_templates_str += '\n' + allowed_response_templates(AgentEnum.ORCHESTRATOR, AgentEnum.SIRJI_USER, permissions_dict[(AgentEnum.ORCHESTRATOR, AgentEnum.SIRJI_USER)]) + '\n'
        allowed_response_templates_str += '\n' +  allowed_response_templates(AgentEnum.ORCHESTRATOR, AgentEnum.ANY, permissions_dict[(AgentEnum.ORCHESTRATOR, AgentEnum.ANY)]) + '\n'

        action_list = permissions_dict[(AgentEnum.ANY, AgentEnum.EXECUTOR)] 
        allowed_response_templates_str += '\n' +  allowed_response_templates(AgentEnum.ANY, AgentEnum.EXECUTOR, action_list) + '\n'        

        current_agent_output_index = f"Current contents of Agent Output Index:\n{json.dumps(self.agent_output_folder_index, indent=4)}"

        return f"{initial_intro}\n{response_specifications}\n{understanding_the_folders}\n{pseudo_code}\n{allowed_response_templates_str}\n{current_agent_output_index}".strip()