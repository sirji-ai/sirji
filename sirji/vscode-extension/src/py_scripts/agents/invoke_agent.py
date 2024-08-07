import argparse
import os
import json
import yaml
import textwrap
from sirji_messages import MessageFactory, ActionEnum, AgentEnum, message_parse
from sirji_agents import GenericAgent
from sirji_tools.logger import create_logger

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

    def read_file(self, file_path):
        print('---------')
        print(file_path)
        with open(file_path, 'r') as file:
            contents = file.read()
        return contents 
  

    def process_input_file(self, input_file_path, conversations):
        with open(input_file_path, 'r') as file:
            contents = file.read()

        self.logger.info(f"Input file contents: {contents}")
        try:
            parsed_content = message_parse(contents)
        except Exception as e:
            parsed_content = None

        if not (parsed_content and parsed_content['ACTION'] == ActionEnum.RESPONSE.name):
            if (len(conversations) > 1 and
                conversations[-1]['parsed_content']['TO'] in [AgentEnum.SIRJI_USER.name, AgentEnum.ORCHESTRATOR.name]):
                
                last_message = conversations[-1]['parsed_content']
                self.logger.info(f"Last message: {last_message}")

                message_class = MessageFactory[ActionEnum.RESPONSE.name]
                contents = message_class().generate({
                    "from_agent_id": last_message['TO'],
                    "to_agent_id": last_message['FROM'],
                    "step": "EMPTY",
                    "summary": "EMPTY",
                    "body": textwrap.dedent(f"""{contents}""")
                })

        self.logger.info(f"Message string: {contents}")
        return contents

    def process_message(self, message_str, conversations, config, agent_output_index, file_summaries):
        agent = GenericAgent(config, agent_output_index, file_summaries)
        return agent.message(message_str, conversations)
        
    def main(self, agent_id, agent_session_id, agent_callstack):
        sirji_installation_dir = os.environ.get("SIRJI_INSTALLATION_DIR")
        sirji_run_path = os.environ.get("SIRJI_RUN_PATH")
        sirji_project_folder = os.environ.get("SIRJI_PROJECT")
        
        input_file_path = os.path.join(sirji_run_path, 'input.txt')
        conversation_file_path = os.path.join(sirji_run_path, 'conversations', f'{agent_callstack}.{agent_session_id}.json')
        agent_output_index_path = os.path.join(sirji_run_path, 'agent_output', 'index.json')

        if agent_id == 'RECIPE_SELECTOR':
                default_path = os.path.join(os.path.dirname(__file__), '../../defaults/agents/RECIPE_SELECTOR.yml')
                agent_path = os.path.join(sirji_installation_dir, 'studio', 'agents', f'{agent_id}.yml')

                if os.path.exists(agent_path):
                    agent_config_path = agent_path
                else:
                    agent_config_path = default_path
        else:
                agent_config_path = os.path.join(sirji_installation_dir, 'studio', 'agents', f'{agent_id}.yml')

        file_summaries_folder_path = os.path.join(sirji_installation_dir, 'file_summaries')
        file_summaries_file_path = os.path.join(file_summaries_folder_path, 'index.json')

        with open(file_summaries_file_path, 'r') as file:
            file_summaries_index = json.load(file)

        relative_path = file_summaries_index.get(sirji_project_folder, '')

        file_summaries = ""

        if relative_path:
            file_summaries_path = os.path.join(file_summaries_folder_path, relative_path)
            if os.path.exists(file_summaries_path):
                with open(file_summaries_path, 'r') as file:
                    file_summaries = file.read()

        config_file_contents = self.read_file(agent_config_path)
        # config = json.loads(config_file_contents)
        config = yaml.safe_load(config_file_contents)

        agent_output_index_contents = self.read_file(agent_output_index_path)
        agent_output_index = json.loads(agent_output_index_contents)

        llm = config['llm']

        self.logger = create_logger(f"{config['id']}.log", 'debug')

        conversations, input_tokens, output_tokens, max_input_tokens_for_a_prompt, max_output_tokens_for_a_prompt =  self.read_or_initialize_conversation_file(conversation_file_path)
        message_str = self.process_input_file(input_file_path, conversations)

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

        response, conversations, prompt_tokens_consumed, completion_tokens_consumed = self.process_message(message_str, conversations, config, agent_output_index, file_summaries)
        
        input_tokens += prompt_tokens_consumed
        output_tokens += completion_tokens_consumed

        max_input_tokens_for_a_prompt = max(max_input_tokens_for_a_prompt, prompt_tokens_consumed)
        max_output_tokens_for_a_prompt = max(max_output_tokens_for_a_prompt, completion_tokens_consumed)
        self.write_conversations_to_file(conversation_file_path, conversations, input_tokens, output_tokens, max_input_tokens_for_a_prompt, max_output_tokens_for_a_prompt, llm['model'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process interactions.")
    parser.add_argument("--agent_id", required=True, help="Agent Id")
    parser.add_argument("--agent_session_id", required=True, help="Agent Session Id")
    parser.add_argument("--agent_callstack", required=True, help="Agent Call Stack")
 
    
    args = parser.parse_args()
    agent_runner = AgentRunner()
    agent_runner.main(args.agent_id, args.agent_session_id, args.agent_callstack)