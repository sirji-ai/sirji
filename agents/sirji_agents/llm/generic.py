import textwrap
import os
import json

# TODO - log file should be dynamically created based on agent ID
from sirji_tools.logger import p_logger as logger

from sirji_messages import message_parse, MessageParsingError, MessageValidationError, ActionEnum
from .model_providers.factory import LLMProviderFactory

class GenericAgent():
    def __init__(self, config, shared_resources_index):

        logger.info('---------inside generic agent-----------')
        logger.info(config)
        logger.info(shared_resources_index)
        
        self.config = config
        self.shared_resources_index = shared_resources_index

    def message(self, input_message, history=[]):
        conversation = self.__prepare_conversation(input_message, history)

        logger.info(f"Incoming: \n{input_message}")
        logger.info("Calling OpenAI Chat Completions API\n")

        response_message, prompt_tokens, completion_tokens = self.__get_response(conversation)

        return response_message, conversation, prompt_tokens, completion_tokens

    def __prepare_conversation(self, input_message, history):
        conversation = []

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
            You are an agent named "{self.config['name']}", a component of the Sirji AI agentic framework.
            Your Agent ID: {self.config['id']}
            Your OS (refered as SIRJI_OS later): {os.name}""")
        
        response_specifications = textwrap.dedent(f"""
            Your Response:
            - Your response must conform strictly to one of the allowed Response Templates, as it will be processed programmatically and only these templates are recognized.
            - Your response must be enclosed within '***' at the beginning and end, without any additional text above or below these markers.
            - Not conforming above rules will lead to response processing errors.
            - Direct each response to one of these recipients (the 'TO' value in the response):
                - SIRJI_USER
                - EXECUTOR
                - ORCHESTRATOR""")
        
        # Todo: Use action names from ActionEnum
        shared_resources = textwrap.dedent(f"""
            Shared Resources:
            Shared Resources folder is a common folder where all agents store their outputs and document these in an index.json file within the folder.
            index.json: A file within the SHARED_RESOURCES_FOLDER that keeps track of all files written by agents along with their descriptions.""")

        instructions = textwrap.dedent(f"""
            Instructions:
            - The ORCHESTRATOR is aware of your skills and has invoked you for a task after finding your skills align with the task's requirements.
            - Upon being invoked, identify which of your skills match the requirements of the task.
            - Execute the sub-tasks associated with each of these matching skills.
            - Do not respond with two actions in the same response. Respond with one action at a time.
            - Always use CREATE_SHARED_RESOURCE_FILE and READ_SHARED_RESOURCES_FILES to write and read files to and from the shared resources folder.                                             
            """)

        formatted_skills = self.__format_skills()

        # TODO: Vaibhav - The Allowed Response Templates part of the agent system prompt must be created dynamically.
        allowed_response_templates = textwrap.dedent("""
            Allowed Response Templates:
            Below are all the possible allowed "Response Template" formats for each of the allowed recipients. You must always respond using one of them.

            Allowed Response Templates TO SIRJI_USER:
            Invoke the SIRJI_USER for the following functions. Please respond with the following, including the starting and ending '***', with no commentary above or below.

            Function 1. Ask a question

            Instructions:
            - Empty

            Response template:
            ***
            FROM: {{Your Agent ID}}
            TO: SIRJI_USER
            ACTION: QUESTION
            SUMMARY: Empty
            BODY:
            {{Question}}
            ***

            Allowed Response Templates TO EXECUTOR:
            Invoke the EXECUTOR for the following functions. Please respond with the following, including the starting and ending '***', with no commentary above or below.

            Function 1. Create a File Inside Workspace Folder Only

            Instructions:
            - The file path must be relative to the workspace root.
            - The file contents should never be enclosed within ``` starting and ending markers.

            Response template:
            ***
            FROM: {{Your Agent ID}}
            TO: EXECUTOR
            ACTION: CREATE_WORKSPACE_FILE
            SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
            BODY:
            File path: {{file path}}
            ---
            {{file contents}}
            ***

            Function 2. Execute a Command, Install Packages, or Install Dependencies

            Instructions:
            - The command must use the workspace root as the current working directory.
            - The command must be sufficiently chained. For example, 'source venv/bin/activate && pip install openai', 'cd server && npm run start'.

            Response template:
            ***
            FROM: {{Your Agent ID}}
            TO: EXECUTOR
            ACTION: EXECUTE_COMMAND
            SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
            BODY:
            {{command}}
            ***

            Function 3: Run a Server or a Continuous Running Process

            Instructions:
            The command must use the workspace root as the current working directory.
            The command must be sufficiently chained. For example, 'source my_env.sh && npm start'.

            Response template:
            ***
            FROM: {{Your Agent ID}}
            TO: EXECUTOR
            ACTION: RUN_SERVER
            SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
            BODY:
            {{command}}
            ***

            Function 4. Read Multiple Files From Workspace Folder Only

            Instructions:
            - The file paths must be relative to the workspace root.

            Response template:
            ***
            FROM: {{Your Agent ID}}
            TO: EXECUTOR
            ACTION: READ_WORKSPACE_FILES
            SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
            BODY:
            File paths: {{Array of file paths}}
            ***

            Function 5. Create a File Inside Shared Resources Folder
                                                                                                                                            
            Instructions:
            - The file path must be in the following format: '{{Your Agent ID}}/{{file name}}'. 
                                                                                    
            Response template:
            ***
            FROM: {{Your Agent ID}}
            TO: EXECUTOR
            ACTION: CREATE_SHARED_RESOURCE_FILE
            SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
            BODY:
            File path: {{file path}}
            ---
            {{file contents}}
            ***
                                                     
            Function 6. Read Multiple Files From Shared Resources

            Instructions:
            - The file paths must be in the following format: '{{Your Agent ID}}/{{file name}}'.

            Response template:
            ***
            FROM: {{Your Agent ID}}
            TO: EXECUTOR
            ACTION: READ_SHARED_RESOURCES_FILES
            SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
            BODY:
            File paths: {{Array of file paths}}
            ***
                                         
            Function 7. Register to the Shared Resource Index
            Instructions:
            - Ensure to register new shared resource files to the shared resources' index.
            - The file path must be in the following format: '{{Your Agent ID}}/{{file name}}'.
                                         
            Response template:
            ***
            FROM: {{Your Agent ID}}
            TO: EXECUTOR
            ACTION: APPEND_TO_SHARED_RESOURCES_INDEX
            SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
            BODY:
            File path: {{file path}}
            ---
            {{Description of the shared resource file, to be used by other agents to know what it is about}}
            ***

            Function 8. Read Shared Resource Index

            Response template:
            ***
            FROM: {{Your Agent ID}}
            TO: EXECUTOR
            ACTION: READ_SHARED_RESOURCE_INDEX
            SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
            BODY:
            Empty
            ***

            Allowed Response Templates TO ORCHESTRATOR:
            Respond to the ORCHESTRATOR at the end of task completion. Please respond with the following, including the starting and ending '***', with no commentary above or below.

            Response template:
            ***
            FROM: {{Installed Agent ID}}
            TO: ORCHESTRATOR
            ACTION: RESPONSE
            SUMMARY: Empty
            BODY:
            {{Task update. Whether the task was done successfully or not. Any other details which you might think are necessary for ORCHESTRATOR to know of.}}
            ***""")
        
        current_shared_resources_index = f"Current contents of shared resources' index.json:\n{json.dumps(self.shared_resources_index, indent=4)}"
        
        return f"{initial_intro}\n{response_specifications}\n{shared_resources}\n{instructions}\n{formatted_skills}\n{allowed_response_templates}\n\n{current_shared_resources_index}".strip()
    
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

        output_text += "Here are your skills with their sub-tasks:\n\n"
        
        # Check if 'skills' exists in the config and is not empty
        if "skills" in self.config and self.config["skills"]:
            for skill in self.config["skills"]:
                output_text += f"Skill: {skill['skill']}\nSubtasks:\n"
                for sub_task in skill["sub_tasks"]:
                    output_text += f"- {sub_task}\n"
                output_text += "\n"
        else:
            output_text += "- No skills provided.\n"

        return output_text

