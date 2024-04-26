import argparse
import os
import json
import textwrap
from sirji_messages import MessageFactory, ActionEnum, AgentEnum
from sirji_agents import OrchestorAgent

class AgentRunner:    
    def _get_workspace_folder(self):
        workspace = os.environ.get("SIRJI_WORKSPACE")
        if workspace is None:
            raise ValueError(
                "SIRJI_WORKSPACE is not set as an environment variable")
        return workspace
    
    def _get_run_id_folder(self):
        run_id = os.environ.get("SIRJI_RUN_ID")
        if run_id is None:
            raise ValueError(
                "SIRJI_RUN_ID is not set as an environment variable")
        return run_id

    def read_or_initialize_conversation_file(self, file_path):
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            with open(file_path, 'w') as file:
                json.dump({"conversations": [], "prompt_tokens": 0, "completion_tokens": 0}, file, indent=4)
                return [], 0, 0
        else:
            with open(file_path, 'r') as file:
                contents = json.load(file)
                return contents["conversations"], contents["prompt_tokens"], contents["completion_tokens"]

    def write_conversations_to_file(self, file_path, conversations, prompt_tokens, completion_tokens):
        with open(file_path, 'w') as file:
            json.dump({"conversations": conversations, "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens}, file, indent=4)

    def read_input_file(self, input_file_path):
        with open(input_file_path, 'r') as file:
            contents = file.read()
        return contents 
  

    def process_input_file(self, input_file_path, conversations):
        with open(input_file_path, 'r') as file:
            contents = file.read()
            message_str = contents

        return message_str

    def process_message(self, message_str, conversations, recipe, installed_agents): 
        agent = OrchestorAgent(recipe, installed_agents)
        return agent.message(message_str, conversations)
        
    def main(self, agent_id):
        ## move to a function   
        sirji_installation_dir = os.environ.get("SIRJI_INSTALLATION_DIR")
        sirji_run_id = os.environ.get("SIRJI_RUN_ID")
        
        input_file_path = os.path.join(sirji_installation_dir, 'Documents', 'Sirji', 'sessions', sirji_run_id, 'inputs', f'{agent_id}.json')
     
        conversation_file_path = os.path.join(sirji_installation_dir, 'Documents', 'Sirji', 'sessions', sirji_run_id, 'conversations', f'{agent_id}.json')

        recipe_file_path = os.path.join(sirji_installation_dir, 'Documents', 'Sirji', 'sessions', sirji_run_id, 'recipes', f'{agent_id}.json')
        
        installed_agent_folder = os.path.join(sirji_installation_dir, 'Documents', 'Sirji', 'agents')


        conversations, prompt_tokens, completion_tokens = self.read_or_initialize_conversation_file(conversation_file_path)
        message_str = self.process_input_file(input_file_path, conversations)

        recipe_file_contents = self.read_input_file(recipe_file_path)
        recipe = json.loads(recipe_file_contents)

        installed_agent_folder_contents = self.read_input_file(installed_agent_folder)
        installed_agents = json.loads(installed_agent_folder_contents)

        response, conversations, prompt_tokens_consumed, completion_tokens_consumed = self.process_message(message_str, conversations, recipe, installed_agents)
        
        prompt_tokens += prompt_tokens_consumed
        completion_tokens += completion_tokens_consumed
        self.write_conversations_to_file(conversation_file_path, conversations, prompt_tokens, completion_tokens)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process interactions.")
    parser.add_argument("--agent_id", required=True, help="Agent Id")
 
    
    args = parser.parse_args()
    agent_runner = AgentRunner()
    agent_runner.main(args.agent_id)