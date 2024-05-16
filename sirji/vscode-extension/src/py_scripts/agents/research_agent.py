import argparse
import os
import json
from sirji_messages import message_parse
from sirji_agents import ResearchAgent

class ResearchAgentRunner:
    def get_workplace_file_path(self, filename):
        return os.path.join(self._get_run_path(), filename)
    
    def _get_project_folder(self):
        project_folder = os.environ.get("SIRJI_PROJECT")
        if project_folder is None:
            raise ValueError(
                "SIRJI_PROJECT is not set as an environment variable")
        return project_folder
    
    def _get_run_path(self):
        run_id = os.environ.get("SIRJI_RUN_PATH")
        if run_id is None:
            raise ValueError(
                "SIRJI_RUN_PATH is not set as an environment variable")
        return run_id 
    
    def read_or_initialize_conversation_file(self, file_path):
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            with open(file_path, 'w') as file:
                json.dump({"conversations": [], "init_payload": {}, "prompt_tokens": 0, "completion_tokens": 0}, file, indent=4)
                return [], {}, 0, 0
        else:
            with open(file_path, 'r') as file:
                contents = json.load(file)
                return contents["conversations"], contents["init_payload"], contents["prompt_tokens"], contents["completion_tokens"]

    def write_conversations_to_file(self, file_path, conversations, init_payload, prompt_tokens, completion_tokens):
        with open(file_path, 'w') as file:
            json.dump({"conversations": conversations, "init_payload": init_payload, "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens}, file, indent=4)

    def process_input_file(self, input_file_path, conversations):
        with open(input_file_path, 'r') as file:
            contents = file.read()
        return contents

    def process_message(self, message_str, conversations, init_payload):
        # Appending the input message to the conversations
        conversations.append({"role": "user", "content": message_str, "parsed_content": message_parse(message_str)})

        researcher = ResearchAgent('openai_assistant', 'openai_assistant', init_payload)

        response, prompt_tokens, completion_tokens = researcher.message(message_str)

        updated_init_payload = researcher.init_payload

        # Updating the init_payload in place, preserving the reference
        init_payload.update(updated_init_payload)

        # Appending the response to the conversations
        conversations.append({"role": "assistant", "content": response, "parsed_content": message_parse(response)})

        return response, prompt_tokens, completion_tokens
        
    def main(self, input_file, conversation_file):
        input_file_path = self.get_workplace_file_path(input_file)
        conversation_file_path = self.get_workplace_file_path(conversation_file)

        conversations, init_payload, prompt_tokens, completion_tokens = self.read_or_initialize_conversation_file(conversation_file_path)

        message_str = self.process_input_file(input_file_path, conversations)

        response, prompt_tokens_consumed, completion_tokens_consumed = self.process_message(message_str, conversations, init_payload)

        prompt_tokens += prompt_tokens_consumed
        completion_tokens += completion_tokens_consumed
        self.write_conversations_to_file(conversation_file_path, conversations, init_payload, prompt_tokens, completion_tokens)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process interactions.")
    parser.add_argument("--input", required=True, help="Input file name")
    parser.add_argument("--conversation", required=True, help="Conversation file name")
    
    args = parser.parse_args()
    agent_runner = ResearchAgentRunner()
    agent_runner.main(args.input, args.conversation)