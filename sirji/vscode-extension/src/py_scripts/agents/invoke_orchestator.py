import argparse
import os
import json
import yaml
from sirji_agents import Orchestrator

class AgentRunner:
    def _get_project_folder(self):
        project_folder = os.environ.get("SIRJI_PROJECT")
        if project_folder is None:
            raise ValueError(
                "SIRJI_PROJECT is not set as an environment variable")
        return project_folder

    def read_or_initialize_conversation_file(self, file_path):
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            with open(file_path, 'w') as file:
                json.dump({"conversations": [], "prompt_tokens": 0, "completion_tokens": 0}, file, indent=4)
                return [], 0, 0
        else:
            with open(file_path, 'r') as file:
                contents = json.load(file)
                return contents["conversations"], contents["prompt_tokens"], contents["completion_tokens"]

    def write_conversations_to_file(self, file_path, conversations, prompt_tokens, completion_tokens, llm_model):
        with open(file_path, 'w') as file:
            json.dump({"conversations": conversations, "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "llm_model": llm_model}, file, indent=4)
            file.flush()
            os.fsync(file.fileno())  # Ensure all internal buffers associated with the file are written to disk

    def read_file(self, input_file_path):
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

    def process_message(self, message_str, conversations, agent_output_index): 
        agent = Orchestrator(agent_output_index)
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
        agent_output_index_path = os.path.join(sirji_run_path, 'agent_output', 'index.json')

        installed_agent_folder = os.path.join(sirji_installation_dir, 'active_recipe', 'agents')
        orchestrator_config_path = os.path.join(installed_agent_folder, f'{agent_id}.yml')
        config_file_contents = self.read_file(orchestrator_config_path)
        config = yaml.safe_load(config_file_contents)

        conversations, prompt_tokens, completion_tokens = self.read_or_initialize_conversation_file(conversation_file_path)
        message_str = self.process_input_file(input_file_path, conversations)

        agent_output_index_contents = self.read_file(agent_output_index_path)
        agent_output_index = json.loads(agent_output_index_contents)

        llm = config['llm']    

        # Set SIRJI_MODEL_PROVIDER env var to llm.provider
        os.environ['SIRJI_MODEL_PROVIDER'] = llm['provider']
        # Set SIRJI_MODEL env var to llm.model
        os.environ['SIRJI_MODEL'] = llm['model']
        
        response, conversations, prompt_tokens_consumed, completion_tokens_consumed = self.process_message(message_str, conversations, agent_output_index)
        
        prompt_tokens += prompt_tokens_consumed
        completion_tokens += completion_tokens_consumed

        self.write_conversations_to_file(conversation_file_path, conversations, prompt_tokens, completion_tokens, llm['model'])

if __name__ == "__main__":
    agent_runner = AgentRunner()
    agent_runner.main('ORCHESTRATOR')