import json
import os
import textwrap

from sirji_messages import ActionEnum, AgentEnum, allowed_response_templates, permissions_dict

class DefaultSystemPrompt:
    def __init__(self, config, agent_output_folder_index):
        self.config = config
        self.agent_output_folder_index = agent_output_folder_index
        pass

    def system_prompt(self):
        initial_intro = textwrap.dedent(f"""
            You are an agent named "{self.config['name']}", a component of the Sirji AI agentic framework. Sirji is a framework that enables developers to create and run custom AI agents for their everyday development tasks. A Custom Agent is a modular AI component that performs specific tasks based on predefined pseudocode.
            Your Agent ID: {self.config['id']}
            Your OS (referred as SIRJI_OS later): {os.name}""")
        
        response_specifications = textwrap.dedent(f"""
            Your Response:
            - Your response must conform strictly to one of the allowed Response Templates, as it will be processed programmatically and only these templates are recognized.
            - Your response must be enclosed within '***' at the beginning and end, without any additional text above or below these markers.
            - Not conforming above rules will lead to response processing errors.""")        
        
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
            - Always use {ActionEnum.STORE_IN_AGENT_OUTPUT.name} and {ActionEnum.READ_AGENT_OUTPUT_FILES.name} to write and read files to and from the agent output folder. 
            - If any step is not applicable or cannot be followed, use the DO_NOTHING action to skip it.                                                                       
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
                    ACTION: {ActionEnum.INVOKE_AGENT.name}
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
                    ACTION: {ActionEnum.INVOKE_AGENT_EXISTING_SESSION.name}
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

        allowed_response_templates_str += textwrap.dedent(f"""For updating in project folder use either {ActionEnum.FIND_AND_REPLACE.name}, {ActionEnum.INSERT_ABOVE.name} or {ActionEnum.INSERT_BELOW.name} actions. Ensure you provide the exact matching string in find from file, with the exact number of lines and proper indentation for insert and replace actions.""") + '\n'
        allowed_response_templates_str += '\n' + allowed_response_templates(AgentEnum.ANY, AgentEnum.CALLER, permissions_dict[(AgentEnum.ANY, AgentEnum.CALLER)]) + '\n'
    
        current_agent_output_index = f"Current contents of Agent Output Index:\n{json.dumps(self.agent_output_folder_index, indent=4)}"

        current_project_folder_structure = f"Recursive structure of the project folder:\n{os.environ.get('SIRJI_PROJECT_STRUCTURE')}"
      
        return f"{initial_intro}\n{response_specifications}{understanding_the_folders}\n{instructions}\n{formatted_skills}\n{allowed_response_templates_str}\n\n{current_agent_output_index}\n\n{current_project_folder_structure}".strip()
    
    def __format_skills(self):
        output_text = ""

        output_text += "Here are your skills details:\n\n"
        
        # Check if 'skills' exists in the config and is not empty
        if "skill" in self.config and self.config["skill"]:
            
            output_text += f"Skill: {self.config['skill']}\n"

            output_text += f"Make sure to first convert all the points mentioned in Pseudo code in plain english to steps having at max 10 words each and log these steps using {ActionEnum.LOG_STEPS.name} action.\n"
            output_text += "Then, execute the steps in the order they are logged.\n"
            output_text += f"Pseudo code which you must follow:\n{self.config['pseudo_code']}"
            output_text += "\n"

        return output_text
