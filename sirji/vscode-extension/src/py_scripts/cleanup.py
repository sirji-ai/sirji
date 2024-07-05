import os
import json
import yaml

from sirji_agents import CleanupFactory

class CleanupHelper:
    
    def _get_run_path(self):
        run_id = os.environ.get("SIRJI_RUN_PATH")
        if run_id is None:
            raise ValueError(
                "SIRJI_RUN_PATH is not set as an environment variable")
        return run_id 

    def read_run_file(self, file_name):
        assistant_details_path = os.path.join(self._get_run_path(), file_name)
        if os.path.exists(assistant_details_path):
            with open(assistant_details_path, 'r') as file:
                return json.load(file)
        else:
            return {}

    def read_file(self, input_file_path):
        with open(input_file_path, 'r') as file:
            contents = file.read()
        return contents
    
    def cleanup_assistant(self, assistant_id):
        cleanup_instance = CleanupFactory.get_instance()
        cleanup_instance.delete_assistant(assistant_id)

    def cleanup_file(self, file_path):
        cleanup_instance = CleanupFactory.get_instance()
        cleanup_instance.delete_file(file_path)

    def cleanup_vector_store(self, vector_store_id):
        cleanup_instance = CleanupFactory.get_instance()
        cleanup_instance.delete_vector_store(vector_store_id)

        assistant_uploaded_files_details = self.read_run_file('assistant_uploaded_files.json')

        if assistant_uploaded_files_details:
            for file_details in assistant_uploaded_files_details:
                self.cleanup_file(file_details['file_id'])

    def main(self):
        sirji_installation_dir = os.environ.get("SIRJI_INSTALLATION_DIR")
        installed_agent_folder = os.path.join(sirji_installation_dir, 'studio', 'agents')
        reasearcher_config_path = os.path.join(installed_agent_folder, f'RESEARCHER.yml')
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

        # Read init_payload from assistant_details.json
        assistant_details = self.read_run_file('assistant_details.json')

        if assistant_details and assistant_details.get('status') == 'active':
            if assistant_details.get('assistant_id'):
                self.cleanup_assistant(assistant_details.get('assistant_id'))
            if assistant_details.get('vector_store_id'):
                self.cleanup_vector_store(assistant_details.get('vector_store_id'))
            # Update the status in assistant_details.json to 'deleted'
            assistant_details['status'] = 'deleted'
            assistant_details_path = os.path.join(self._get_run_path(), 'assistant_details.json')
            with open(assistant_details_path, 'w') as file:
                json.dump(assistant_details, file)
        else:
            print("Assistant is not active. No cleanup required.")
    
        
if __name__ == "__main__":
    runner = CleanupHelper()
    runner.main()