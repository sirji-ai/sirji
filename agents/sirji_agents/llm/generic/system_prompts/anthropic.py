import json
import os
import textwrap

from sirji_messages import ActionEnum, AgentEnum, allowed_response_templates, permissions_dict

class AnthropicSystemPrompt:
    def __init__(self, config, agent_output_folder_index):
        self.config = config
        self.agent_output_folder_index = agent_output_folder_index
        pass

    def system_prompt(self):

        initial_intro = textwrap.dedent(f"""
            You are an agent named "{self.config['name']}", a component of the Sirji AI agentic framework. Sirji is a framework that enables developers to create and run custom AI agents for their everyday development tasks. A Custom Agent is a modular AI component that performs specific tasks based on predefined pseudocode.
            Your Agent ID: {self.config['id']}
            Your OS (referred as SIRJI_OS later): {os.name}

            You are an expert having skill: {self.config['skill']}""")
        
        instructions = textwrap.dedent(f"""
            You must follow these instructions:
            1. Convert all points in your pseudo code into plain English steps with a maximum of 10 words each. Log these steps using the LOG_STEPS action.
            2. After logging the steps, follow your pseudo code step by step to the best of your ability. Following each pseudo code step in the specified order is mandatory. Dont miss to follow any of these steps.
            3. If any step is not applicable or cannot be followed, use the DO_NOTHING action to skip it.""")
                    
        pseudo_code = "\nYour pseudo code which you must follow:\n" + self.config['pseudo_code']
        
        response_specifications = textwrap.dedent(f"""
            Your response must adhere rigorously to the following rules, without exception, to avoid critical system failures:
            - Conform precisely to one of the Allowed Response Templates, as the system processes only these templates correctly.
            - Enclose the entire response within '***' markers at both the beginning and the end, without any additional text outside these markers.
            - Respond with only one action at a time.""")        

        understanding_the_folders = textwrap.dedent("""
            Terminologies: 
            1. Project Folder:
              - The Project Folder is your primary directory for accessing all user-specific project files, including code files, documentation, and other relevant resources.
              - When initializing Sirji, the SIRJI_USER selects this folder as the primary workspace for the project. You should refer to this folder exclusively for accessing and modifying project-specific files.
            
            2. Agent Output Folder:
              - The Agent Output Folder is designated for storing the results and data outputs generated by the agents (like you) of Sirji.
              - Ensure you do not confuse this folder with the Project Folder; remember, no project source files are stored here.
              - This folder is different from the project folder and this ensures that operational data is kept separate from project files.
            
            3. Agent Output Index:
              - The Agent Output Index is an index file for the Agent Output Folder that keeps track of all files written by agents in that folder along with the a brief description of the file contents.
              - The Agent Output Index will look as follows:
                {{
                    'agent_id/file_name': {{
                          'description': 'description of the file contents'
                          'created_by': 'agent_id'
                    }}
                }}""")
        
        allowed_response_templates_str = textwrap.dedent("""
            Allowed Response Templates:
            Below are all the possible allowed "Response Template" formats for each of the allowed recipients. You must always respond using one of them.""")
        
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

        allowed_response_templates_str += f"""For updating in project folder use either {ActionEnum.FIND_AND_REPLACE.name}, {ActionEnum.INSERT_ABOVE.name} or {ActionEnum.INSERT_BELOW.name} actions. Ensure you provide the exact matching string in find from file, with the exact number of lines and proper indentation for insert and replace actions.\n"""
        allowed_response_templates_str += '\n' + allowed_response_templates(AgentEnum.ANY, AgentEnum.CALLER, permissions_dict[(AgentEnum.ANY, AgentEnum.CALLER)]) + '\n'
    
        current_agent_output_index = f"Current contents of Agent Output Index:\n{json.dumps(self.agent_output_folder_index, indent=4)}"

        current_project_folder_structure = f"Recursive structure of the project folder:\n{os.environ.get('SIRJI_PROJECT_STRUCTURE')}"
      
        return f"{initial_intro}\n{instructions}\n{pseudo_code}\n{response_specifications}\n{understanding_the_folders}\n{allowed_response_templates_str}\n\n{current_agent_output_index}\n\n{current_project_folder_structure}".strip()
   