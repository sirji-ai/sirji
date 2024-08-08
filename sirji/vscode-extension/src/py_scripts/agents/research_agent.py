import argparse
import os
import json
import yaml

from sirji_messages import message_parse
from sirji_agents import ResearchAgent

class ResearchAgentRunner:
    
    def _get_run_path(self):
        run_id = os.environ.get("SIRJI_RUN_PATH")
        if run_id is None:
            raise ValueError(
                "SIRJI_RUN_PATH is not set as an environment variable")
        return run_id 
    

    def read_or_initialize_conversation_file(self, file_path):
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            with open(file_path, 'w') as file:
                json.dump({"conversations": [], "input_tokens": 0, "output_tokens": 0, "max_input_tokens_for_a_prompt": 0, "max_output_tokens_for_a_prompt": 0}, file, indent=4)
                return [], 0, 0, 0, 0
        else:
            with open(file_path, 'r') as file:
                contents = json.load(file)
                return contents["conversations"], contents["input_tokens"], contents["output_tokens"], contents["max_input_tokens_for_a_prompt"], contents["max_output_tokens_for_a_prompt"]

    def read_assistant_details(self):
        assistant_details_path = os.path.join(self._get_run_path(), 'assistant_details.json')
        if os.path.exists(assistant_details_path):
            with open(assistant_details_path, 'r') as file:
                return json.load(file)
        else:
            return {}

    def write_conversations_to_file(self, file_path, conversations, input_tokens, output_tokens, max_input_tokens_for_a_prompt, max_output_tokens_for_a_prompt, llm_model):
        with open(file_path, 'w') as file:
            json.dump({"conversations": conversations, "input_tokens": input_tokens, "output_tokens": output_tokens, "max_input_tokens_for_a_prompt": max_input_tokens_for_a_prompt, "max_output_tokens_for_a_prompt": max_output_tokens_for_a_prompt, "llm_model": llm_model}, file, indent=4)
            file.flush()
            os.fsync(file.fileno())  # Ensure all internal buffers associated with the file are written to disk

    def process_input_file(self, input_file_path, conversations):
        if not os.path.exists(input_file_path):
            with open(input_file_path, 'w') as file:
                json.dump({}, file, indent=4)
        
        with open(input_file_path, 'r') as file:
            contents = file.read()
            message_str = contents

        return message_str

    def process_message(self, message_str, conversations, init_payload):
        # Appending the input message to the conversations
        conversations.append({"role": "user", "content": message_str, "parsed_content": message_parse(message_str)})

        researcher = ResearchAgent(init_payload)

        response, prompt_tokens, completion_tokens = researcher.message(message_str)

        print(f"Response: {response}")

        # Appending the response to the conversations
        conversations.append({"role": "assistant", "content": response, "parsed_content": message_parse(response)})

        return response, prompt_tokens, completion_tokens
    

    def read_file(self, input_file_path):
        with open(input_file_path, 'r') as file:
            contents = file.read()
        return contents
        
    def main(self, agent_id, agent_session_id, agent_callstack):
        sirji_installation_dir = os.environ.get("SIRJI_INSTALLATION_DIR")
        sirji_run_path = os.environ.get("SIRJI_RUN_PATH")

        print(f"Running Research Agent with agent_id: {agent_id}")
        print(f"Using SIRJI_RUN_PATH: {sirji_run_path}")

        input_file_path = os.path.join(sirji_run_path, 'input.txt')
        conversation_file_path = os.path.join(sirji_run_path, 'conversations', f'{agent_id}.json')

        default_path = os.path.join(os.path.dirname(__file__), '../../defaults/agents/RESEARCHER.yml')
        agent_path = os.path.join(sirji_installation_dir, 'studio', 'agents', f'{agent_id}.yml')

        if os.path.exists(agent_path):
            agent_config_path = agent_path
        else:
            agent_config_path = default_path

        config_file_contents = self.read_file(agent_config_path)
        config = yaml.safe_load(config_file_contents)

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

        conversations, input_tokens, output_tokens, max_input_tokens_for_a_prompt, max_output_tokens_for_a_prompt =  self.read_or_initialize_conversation_file(conversation_file_path)
        message_str = self.process_input_file(input_file_path, conversations)

        # Read init_payload from assistant_details.json
        assistant_details = self.read_assistant_details()

        init_payload = assistant_details
        init_payload['complete_session_id'] = agent_callstack + '.' + agent_session_id
       
        response, prompt_tokens_consumed, completion_tokens_consumed = self.process_message(message_str, conversations, init_payload)

        input_tokens += prompt_tokens_consumed
        output_tokens += completion_tokens_consumed

        max_input_tokens_for_a_prompt = max(max_input_tokens_for_a_prompt, prompt_tokens_consumed)
        max_output_tokens_for_a_prompt = max(max_output_tokens_for_a_prompt, completion_tokens_consumed)

        self.write_conversations_to_file(conversation_file_path, conversations, input_tokens, output_tokens, max_input_tokens_for_a_prompt, max_output_tokens_for_a_prompt, 'gpt-4o')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process interactions.")
    parser.add_argument("--agent_session_id", required=True, help="Agent Session Id")
    parser.add_argument("--agent_callstack", required=True, help="Agent Call Stack")


    args = parser.parse_args()
    agent_runner = ResearchAgentRunner()
    agent_runner.main('RESEARCHER',args.agent_session_id, args.agent_callstack)
    