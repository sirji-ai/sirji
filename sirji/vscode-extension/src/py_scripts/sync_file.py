
import argparse;
import os;
import json;
import yaml;

from sirji_agents import ResearchAgent;

class SyncFile:

  def read_assistant_details(self, file_path):
    assistant_details_path = os.path.join(self._get_run_path(), 'assistant_details.json')
    if os.path.exists(assistant_details_path):
        with open(assistant_details_path, 'r') as file:
            return json.load(file)
    else:
        return {}

  def main(self, file_path):

    sirji_installation_dir = os.environ.get("SIRJI_INSTALLATION_DIR")
   
    agent_id = "RESEARCHER"
    installed_agent_folder = os.path.join(sirji_installation_dir, 'studio', 'agents')
    reasearcher_config_path = os.path.join(installed_agent_folder, f'{agent_id}.yml')
    config_file_contents = self.read_file(reasearcher_config_path)
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
  
    assistant_details = self.read_assistant_details()
    researcher = ResearchAgent(assistant_details)
    response = researcher._sync_file(file_path)

    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process interactions.")
    parser.add_argument("--file_path", required=True, help="Agent Id")
    args = parser.parse_args()
    agent_runner = SyncFile()
    agent_runner.main(args.file_path)