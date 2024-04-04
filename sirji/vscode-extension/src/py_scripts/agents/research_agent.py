import argparse
import os
import json
from sirji_messages import message_parse
from sirji_agents import ResearchAgent

class ResearchAgentRunner:
    def get_workplace_file_path(self, filename):
        return os.path.join(self._get_workspace_folder(), '.sirji', filename)
    
    def _get_workspace_folder(self):
        workspace = os.environ.get("SIRJI_WORKSPACE")
        if workspace is None:
            raise ValueError(
                "SIRJI_WORKSPACE is not set as an environment variable")
        return workspace

    def read_or_initialize_conversation_file(self, file_path):
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            with open(file_path, 'w') as file:
                json.dump({"conversations": [], "init_payload": {}}, file, indent=4)
                return [], {}
        else:
            with open(file_path, 'r') as file:
                contents = json.load(file)
                return contents["conversations"], contents["init_payload"]

    def write_conversations_to_file(self, file_path, conversations, init_payload):
        with open(file_path, 'w') as file:
            json.dump({"conversations": conversations, "init_payload": init_payload}, file, indent=4)

    def process_input_file(self, input_file_path, conversations):
        with open(input_file_path, 'r') as file:
            contents = file.read()
        return contents

    def process_message(self, message_str, conversations, init_payload):
        # Appending the input message to the conversations
        conversations.append({"role": "user", "content": message_str, "parsed_content": message_parse(message_str)})

        researcher = ResearchAgent('openai_assistant', 'openai_assistant', init_payload)

        response = researcher.message(message_str)

        updated_init_payload = researcher.init_payload

        # Updating the init_payload in place, preserving the reference
        init_payload.update(updated_init_payload)

        # Appending the response to the conversations
        conversations.append({"role": "assistant", "content": response, "parsed_content": message_parse(response)})

        return response
        
    def main(self, input_file, conversation_file):
        input_file_path = self.get_workplace_file_path(input_file)
        conversation_file_path = self.get_workplace_file_path(conversation_file)

        conversations, init_payload = self.read_or_initialize_conversation_file(conversation_file_path)
        message_str = self.process_input_file(input_file_path, conversations)

        response = self.process_message(message_str, conversations, init_payload)
        self.write_conversations_to_file(conversation_file_path, conversations, init_payload)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process interactions.")
    parser.add_argument("--input", required=True, help="Input file name")
    parser.add_argument("--conversation", required=True, help="Conversation file name")
    
    args = parser.parse_args()
    agent_runner = ResearchAgentRunner()
    agent_runner.main(args.input, args.conversation)