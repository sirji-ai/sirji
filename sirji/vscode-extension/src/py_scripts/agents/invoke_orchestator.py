import argparse
import os
import json
from sirji_agents import Orchestrator

class AgentRunner:
    def _get_workspace_folder(self):
        workspace = os.environ.get("SIRJI_WORKSPACE")
        if workspace is None:
            raise ValueError(
                "SIRJI_WORKSPACE is not set as an environment variable")
        return workspace

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
            file.flush()
            os.fsync(file.fileno())  # Ensure all internal buffers associated with the file are written to disk

    def read_input_file(self, input_file_path):
        with open(input_file_path, 'r') as file:
            contents = file.read()
        return contents
  

    def process_input_file(self, input_file_path, conversations):
        if not os.path.exists(input_file_path):
            with open(input_file_path, 'w') as file:
                json.dump({}, file, indent=4)
        
        with open(input_file_path, 'r') as file:
            contents = file.read()
            message_str = contents

        return message_str

    def process_message(self, message_str, conversations, recipe, installed_agents): 
        agent = Orchestrator(recipe, installed_agents)
        return agent.message(message_str, conversations)
    
    def read_agents_from_files(self, directory):
        installed_agents = []
        
        # Loop through each file in the directory
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                file_path = os.path.join(directory, filename)
                
                # Read and parse the JSON file
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    
                    # Extract the required information
                    agent = {
                        "id": data["id"],
                        "name": data["name"],
                        "skills": [skill["skill"] for skill in data["skills"]]
                    }
                    
                    # Append the agent object to the list
                    installed_agents.append(agent)
        
        return installed_agents
        
    def main(self, agent_id):
        ## move to a function   
        sirji_installation_dir = os.environ.get("SIRJI_INSTALLATION_DIR")
        sirji_run_path = os.environ.get("SIRJI_RUN_PATH")

        input_file_path = os.path.join(sirji_run_path, 'input.txt')
        conversation_file_path = os.path.join(sirji_run_path, 'conversations', f'{agent_id}.json')
        shared_resources_index_path = os.path.join(sirji_run_path, 'shared_resources', 'index.json')

        recipe_file_path = os.path.join(sirji_installation_dir, 'recipe.json')
        installed_agent_folder = os.path.join(sirji_installation_dir, 'installed_agents')

        installed_agents = self.read_agents_from_files(installed_agent_folder)

        conversations, prompt_tokens, completion_tokens = self.read_or_initialize_conversation_file(conversation_file_path)
        message_str = self.process_input_file(input_file_path, conversations)

        recipe_file_contents = self.read_input_file(recipe_file_path)
        recipe = json.loads(recipe_file_contents)

        response, conversations, prompt_tokens_consumed, completion_tokens_consumed = self.process_message(message_str, conversations, recipe, installed_agents)
        
        prompt_tokens += prompt_tokens_consumed
        completion_tokens += completion_tokens_consumed
        self.write_conversations_to_file(conversation_file_path, conversations, prompt_tokens, completion_tokens)

if __name__ == "__main__":
    agent_runner = AgentRunner()
    agent_runner.main('ORCHESTRATOR')