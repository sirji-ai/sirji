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
                json.dump({"conversations": [], "input_tokens": 0, "output_tokens": 0, "max_input_tokens_for_a_prompt": 0, "max_output_tokens_for_a_prompt": 0}, file, indent=4)
                return [], 0, 0, 0, 0
        else:
            with open(file_path, 'r') as file:
                contents = json.load(file)
                return contents["conversations"], contents["input_tokens"], contents["output_tokens"], contents["max_input_tokens_for_a_prompt"], contents["max_output_tokens_for_a_prompt"]

    def write_conversations_to_file(self, file_path, conversations, input_tokens, output_tokens, max_input_tokens_for_a_prompt, max_output_tokens_for_a_prompt, llm_model):
        with open(file_path, 'w') as file:
            json.dump({"conversations": conversations, "input_tokens": input_tokens, "output_tokens": output_tokens, "max_input_tokens_for_a_prompt": max_input_tokens_for_a_prompt, "max_output_tokens_for_a_prompt": max_output_tokens_for_a_prompt, "llm_model": llm_model}, file, indent=4)
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

        default_path = os.path.join(os.path.dirname(__file__), '../../defaults/agents/ORCHESTRATOR.yml')
        agent_path = os.path.join(sirji_installation_dir, 'studio', 'agents', f'{agent_id}.yml')

        if os.path.exists(agent_path):
            agent_config_path = agent_path
        else:
            agent_config_path = default_path

        config_file_contents = self.read_file(agent_config_path)
        
        config = yaml.safe_load(config_file_contents)

        conversations, input_tokens, output_tokens, max_input_tokens_for_a_prompt, max_output_tokens_for_a_prompt =  self.read_or_initialize_conversation_file(conversation_file_path)
        message_str = self.process_input_file(input_file_path, conversations)

        agent_output_index_contents = self.read_file(agent_output_index_path)
        agent_output_index = json.loads(agent_output_index_contents)

        llm = config['llm']    

        # Set SIRJI_MODEL_PROVIDER env var to llm.provider
        os.environ['SIRJI_MODEL_PROVIDER'] = llm['provider']
        # Set SIRJI_MODEL env var to llm.model
        os.environ['SIRJI_MODEL'] = llm['model']
        if llm['provider'] == 'openai':
            os.environ['SIRJI_MODEL_PROVIDER_API_KEY'] = os.environ.get('SIRJI_OPENAI_API_KEY')
        elif llm['provider'] == 'deepseek':
            os.environ['SIRJI_MODEL_PROVIDER_API_KEY'] = os.environ.get('SIRJI_DEEPSEEK_API_KEY')
        elif llm['provider'] == 'anthropic':
            os.environ['SIRJI_MODEL_PROVIDER_API_KEY'] = os.environ.get('SIRJI_ANTHROPIC_API_KEY')
        
        response, conversations, prompt_tokens_consumed, completion_tokens_consumed = self.process_message(message_str, conversations, agent_output_index)
        
        input_tokens += prompt_tokens_consumed
        output_tokens += completion_tokens_consumed

        max_input_tokens_for_a_prompt = max(max_input_tokens_for_a_prompt, prompt_tokens_consumed)
        max_output_tokens_for_a_prompt = max(max_output_tokens_for_a_prompt, completion_tokens_consumed)

        self.write_conversations_to_file(conversation_file_path, conversations, input_tokens, output_tokens, max_input_tokens_for_a_prompt, max_output_tokens_for_a_prompt, llm['model'])

if __name__ == "__main__":
    agent_runner = AgentRunner()
    agent_runner.main('ORCHESTRATOR')