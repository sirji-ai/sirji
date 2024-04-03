import argparse
import os
import json

class AgentRunnerBase:
    def get_workplace_file_path(self, filename):
        workspace = os.environ.get("SIRJI_WORKSPACE", "")
        return os.path.join(workspace, filename)

    def read_or_initialize_conversation_file(self, file_path):
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            with open(file_path, 'w') as file:
                json.dump({"conversations": []}, file, indent=4)
                return []
        else:
            with open(file_path, 'r') as file:
                return json.load(file)["conversations"]

    def write_conversations_to_file(self, file_path, conversations):
        with open(file_path, 'w') as file:
            json.dump({"conversations": conversations}, file, indent=4)

    def main(self, input_file, conversation_file):
        input_file_path = self.get_workplace_file_path(input_file)
        conversation_file_path = self.get_workplace_file_path(conversation_file)

        conversations = self.read_or_initialize_conversation_file(conversation_file_path)
        message_str = self.process_input_file(input_file_path, conversations)

        # Agent-specific behavior will be implemented in the child classes
        response, conversations = self.process_message(message_str, conversations)
        self.write_conversations_to_file(conversation_file_path, conversations)

    # To be implemented by subclasses
    def process_message(self, message_str, conversations):
        raise NotImplementedError

    def process_input_file(self, input_file_path, conversations):
        # This method will be overridden in child classes
        raise NotImplementedError