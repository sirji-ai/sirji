import textwrap
import os
import json

# TODO - log file should be dynamically created based on agent ID
from sirji_tools.logger import create_logger
from sirji_messages import message_parse, MessageParsingError, MessageValidationError, ActionEnum, AgentEnum, allowed_response_templates, permissions_dict, ActionEnum
from .model_providers.factory import LLMProviderFactory

class GenericAgent():
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
                self.logger.info("Error while parsing the message.\n")
                retry_llm_count += 1
                if retry_llm_count > 2:
                    raise e
                self.logger.info(f"Requesting LLM to resend the message in correct format.\n")
                conversation.append({"role": "assistant", "content": response_message, "parsed_content": {}})
                conversation.append({"role": "user", "content": "Error in processing your last response. Your response must conform strictly to one of the allowed Response Templates, as it will be processed programmatically and only these templates are recognized. Your response must be enclosed within '***' at the beginning and end, without any additional text above or below these markers. Not conforming above rules will lead to response processing errors."})
            except Exception as e:
                self.logger.info(f"Generic error while parsing message. Error: {e}\n")
                raise e
                        
        return response_message, prompt_tokens, completion_tokens
    
    def __call_llm(self, conversation):
        history = []

        for message in conversation:
            history.append({"role": message['role'], "content": message['content']})

        model_provider = LLMProviderFactory.get_instance()

        return model_provider.get_response(history, self.logger)

    def system_prompt(self):
        initial_intro = textwrap.dedent(f"""
            You are an agent named "{self.config['name']}", a component of the Sirji AI agentic framework.
            Your Agent ID: {self.config['id']}
            Your OS (referred as SIRJI_OS later): {os.name}""")
        
        response_specifications = textwrap.dedent(f"""
            Your Response:
            - Your response must conform strictly to one of the allowed Response Templates, as it will be processed programmatically and only these templates are recognized.
            - Your response must be enclosed within '***' at the beginning and end, without any additional text above or below these markers.
            - Not conforming above rules will lead to response processing errors.""")        
        # Todo: Use action names from ActionEnum
        understanding_the_folders = textwrap.dedent("""
            Project Folder:
            - The Project Folder is your primary directory for accessing all user-specific project files, including code files, documentation, and other relevant resources.
            - When initializing Sirji, the SIRJI_USER selects this folder as the primary workspace for the project. You should refer to this folder exclusively for accessing and modifying project-specific files.
            
            Agent Output Folder:
            - The Agent Output Folder is designated for storing the results and data outputs generated by the agents (like you) of Sirji.
            - Ensure you do not confuse this folder with the Project Folder; remember, no project source files are stored here.
            - This folder is different from the project folder and this ensures that operational data is kept separate from project files.
            
            Agent Output Index:
            - The Agent Output Index is an index file for the Agent Output Folder that keeps track of all files written by agents in that folder along with the a brief description of the file contents.
            - The Agent Output Index will look as follows:
              {
                  'agent_id/file_name': {
                        'description': 'description of the file contents'
                        'created_by': 'agent_id'
                  }
              }""")

        instructions = textwrap.dedent(f"""
            Instructions:
            - You have the skill which match with the task's requirements.
            - Upon being invoked, identify which of your skills match the requirements of the task.
            - Execute the sub-tasks associated with each of these matching skills.
            - Do not respond with two actions in the same response. Respond with one action at a time.
            - Always use STORE_IN_AGENT_OUTPUT and READ_AGENT_OUTPUT_FILES to write and read files to and from the agent output folder.                                             
            """)

        formatted_skills = self.__format_skills()
        allowed_response_templates_str = textwrap.dedent("""
            Allowed Response Templates:
            Below are all the possible allowed "Response Template" formats for each of the allowed recipients. You must always respond using one of them.
            """)
        
        if "sub_agents" in self.config and self.config["sub_agents"]:
            for sub_agent in self.config["sub_agents"]:
            
                allowed_response_templates_str += textwrap.dedent(f"""
                    Allowed Response Templates to {sub_agent['id']}:
                    For invoking the {sub_agent['id']}, in a fresh session, use the following response template. Please respond with the following, including the starting and ending '***', with no commentary above or below.
                    
                    Response template:
                    ***
                    FROM: {{Your Agent ID}}
                    TO: {sub_agent['id']}
                    ACTION: INVOKE_AGENT
                    STEP: "provide the step number here for the ongoing step if any."
                    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
                    BODY:
                    {{Purpose of invocation.}}
                    ***""") + '\n'
                
                allowed_response_templates_str += textwrap.dedent(f"""
                    For invoking the {sub_agent['id']}, continuing over the existing session session, use the following response template. Please respond with the following, including the starting and ending '***', with no commentary above or below.
                    
                    Response template:
                    ***
                    FROM: {{Your Agent ID}}
                    TO: {sub_agent['id']}
                    ACTION: INVOKE_AGENT_EXISTING_SESSION
                    STEP: "provide the step number here for the ongoing step if any."
                    SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
                    BODY:
                    {{Purpose of invocation.}}
                    ***""") + '\n'
            
        allowed_response_templates_str += '\n' + allowed_response_templates(AgentEnum.ANY, AgentEnum.SIRJI_USER, permissions_dict[(AgentEnum.ANY, AgentEnum.SIRJI_USER)]) + '\n'

        action_list = permissions_dict[(AgentEnum.ANY, AgentEnum.EXECUTOR)]
        accessible_actions = self.config.get("accessible_actions", [])
        if accessible_actions:
            for action in accessible_actions:
                action_list.add(ActionEnum[action])
        allowed_response_templates_str += '\n' +  allowed_response_templates(AgentEnum.ANY, AgentEnum.EXECUTOR, action_list) + '\n'

        allowed_response_templates_str += "For updating in project folder use either FIND_AND_REPLACE, INSERT_ABOVE or INSERT_BELOW actions. Ensure you provide the exact matching string in find from file, with the exact number of lines and proper indentation for insert and replace actions.\n"
        allowed_response_templates_str += '\n' + allowed_response_templates(AgentEnum.ANY, AgentEnum.CALLER, permissions_dict[(AgentEnum.ANY, AgentEnum.CALLER)]) + '\n'
    
        current_agent_output_index = f"Current contents of Agent Output Index:\n{json.dumps(self.agent_output_folder_index, indent=4)}"

        current_project_folder_structure = f"Recursive structure of the project folder:\n{os.environ.get('SIRJI_PROJECT_STRUCTURE')}"
        file_summaries = ""
        if self.file_summaries:
            file_summaries = 'Here are the concise summaries of the responsibilities and functionalities for each file currently present in the project folder:\n'
            file_summaries += f"File Summaries:\n{self.file_summaries}"
        

        return f"{initial_intro}\n{response_specifications}{understanding_the_folders}\n{instructions}\n{formatted_skills}\n{allowed_response_templates_str}\n\n{current_agent_output_index}\n\n{current_project_folder_structure}\n\n{file_summaries}".strip()
    
    def __format_skills(self):
        output_text = ""
        
        # Check if 'definitions' exists in the config and is not empty
        if "definitions" in self.config and self.config["definitions"]:
            output_text += "The definitions to be used for executing sub-tasks of your skills:\n"

            for key, value in self.config["definitions"].items():
                output_text += f"- {key}: {value}\n"
        
            output_text += "\n"
        
        # Check if 'rules' exists in the config and is not empty
        if "rules" in self.config and self.config["rules"]:
            output_text += "The rules that must be followed for executing sub-tasks of your skills:\n"
            for rule in self.config["rules"]:
                output_text += f"- {rule}\n"
        
            output_text += "\n"

        output_text += "Here are your skills details:\n\n"
        
        # Check if 'skills' exists in the config and is not empty
        if "skills" in self.config and self.config["skills"]:
            for skill in self.config["skills"]:
                output_text += f"Skill: {skill['skill']}\n"

                if "sub_tasks" in skill and skill["sub_tasks"]:
                    output_text += "Subtasks:\n"
                    for sub_task in skill["sub_tasks"]:
                        output_text += f"- {sub_task}\n"
                    output_text += "\n"
                elif "pseudo_code" in skill and skill['pseudo_code']:
                    output_text += "Make sure to first convert all the points mentioned in Pseudo code in plain english to steps having at max 10 words each and log these steps using LOG_STEPS action.\n"
                    output_text += "Then, execute the steps in the order they are logged.\n"
                    output_text += f"Pseudo code which you must follow:\n{skill['pseudo_code']}"
                    output_text += "\n"
                                   

        return output_text

