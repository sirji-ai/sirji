import argparse
import os
import json
import textwrap
from sirji_messages import MessageFactory, ActionEnum, AgentEnum
from sirji_agents import GenericAgent

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

    def read_input_file(self, input_file_path):
        with open(input_file_path, 'r') as file:
            contents = file.read()
        return contents 
  

    def process_input_file(self, input_file_path, conversations):
        with open(input_file_path, 'r') as file:
            contents = file.read()

        if conversations[-1]['parsed_content']['TO'] in [AgentEnum.USER.name, AgentEnum.EXECUTOR.name, AgentEnum.ORCHESTRATOR.name]:
            last_action = conversations[-1]['parsed_content']
            
            message_class = MessageFactory[ActionEnum.RESPONSE.name]
            message_str = message_class().generate({
            "from_agent_id": "{last_action.TO}",
            "to_agent_id": "{last_action.FROM}",
            "summary": "EMPTY",
            "body": textwrap.dedent("""
            {contents}
            """)})
        else:
            message_str = contents

        return message_str

    def process_message(self, message_str, conversations, config, shared_resources_index): 
        agent = GenericAgent(config, shared_resources_index)
        return agent.message(message_str, conversations)
        
    def main(self, agent_id):  
        sirji_installation_dir = os.environ.get("SIRJI_INSTALLATION_DIR")
        sirji_run_path = os.environ.get("SIRJI_RUN_PATH")
        
        input_file_path = os.path.join(sirji_run_path, 'inputs', f'{agent_id}.json')
        conversation_file_path = os.path.join(sirji_run_path, 'conversations', f'{agent_id}.json')
        shared_resources_index_path = os.path.join(sirji_run_path, 'shared_resources', 'index.json')
        
        agent_config_path = os.path.join(sirji_installation_dir, 'installed_agents', f'{agent_id}.json')

        conversations, prompt_tokens, completion_tokens = self.read_or_initialize_conversation_file(conversation_file_path)
        message_str = self.process_input_file(input_file_path, conversations)

        config_file_contents = self.read_input_file(agent_config_path)
        config = json.loads(config_file_contents)

        shared_resources_index_contents = self.read_input_file(shared_resources_index_path)
        shared_resources_index = json.loads(shared_resources_index_contents)

        response, conversations, prompt_tokens_consumed, completion_tokens_consumed = self.process_message(message_str, conversations, config, shared_resources_index)
        
        prompt_tokens += prompt_tokens_consumed
        completion_tokens += completion_tokens_consumed
        self.write_conversations_to_file(conversation_file_path, conversations, prompt_tokens, completion_tokens)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process interactions.")
    parser.add_argument("--agent_id", required=True, help="Agent Id")
 
    
    args = parser.parse_args()
    agent_runner = AgentRunner()
    agent_runner.main(args.agent_id)