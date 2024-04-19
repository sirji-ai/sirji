import argparse
import os
import json
from sirji_messages import MessageFactory, ActionEnum, AgentEnum
from sirji_agents import CodingAgent

class CodingAgentRunner:
    def get_workplace_file_path(self, filename):
        return os.path.join(self._get_workspace_folder(), '.sirji', self._get_run_id_folder(), filename)
    
    def _get_workspace_folder(self):
        workspace = os.environ.get("SIRJI_WORKSPACE")
        if workspace is None:
            raise ValueError(
                "SIRJI_WORKSPACE is not set as an environment variable")
        return workspace
    
    def _get_run_id_folder(self):
        run_id = os.environ.get("SIRJI_RUN_ID")
        if run_id is None:
            raise ValueError(
                "SIRJI_RUN_ID is not set as an environment variable")
        return run_id

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
  

    def process_input_file(self, input_file_path, conversations):
        with open(input_file_path, 'r') as file:
            contents = file.read()

        if not conversations:
            message_class = MessageFactory[ActionEnum.PROBLEM_STATEMENT.name]
            message_str = message_class().generate({"details": contents})
        elif conversations[-1]['parsed_content']['TO'] == AgentEnum.USER.name:
            last_action = conversations[-1]['parsed_content']['ACTION']

            if last_action in [ActionEnum.INFORM.name, ActionEnum.QUESTION.name]:
                message_class = MessageFactory[ActionEnum.ANSWER.name]
                message_str = message_class().generate({"details": contents})
            elif last_action == ActionEnum.SOLUTION_COMPLETE.name:
                message_class = MessageFactory[ActionEnum.FEEDBACK.name]
                message_str = message_class().generate({"details": contents})
            elif last_action in [ActionEnum.STEP_STARTED.name, ActionEnum.STEP_COMPLETED.name]:
                message_class = MessageFactory[ActionEnum.ACKNOWLEDGE.name]
                message_str = message_class().generate({"details": contents})
                print(f"Message: {message_str}")
            else:
                raise ValueError(f"Invalid action: {last_action}")
        elif conversations[-1]['parsed_content']['TO'] == AgentEnum.EXECUTOR.name:
            last_action = conversations[-1]['parsed_content']['ACTION']

            if last_action in [ActionEnum.EXECUTE_COMMAND.name, ActionEnum.RUN_SERVER.name, ActionEnum.CREATE_FILE.name, ActionEnum.INSTALL_PACKAGE.name, ActionEnum.READ_FILE.name, ActionEnum.READ_DIR.name, ActionEnum.READ_DIR_STRUCTURE.name]:
                message_class = MessageFactory[ActionEnum.OUTPUT.name]
                message_str = message_class().generate({"details": contents})
            else:
                raise ValueError(f"Invalid action: {last_action}")
        else:
            message_str = contents

        return message_str

    def process_message(self, message_str, conversations):
        coder = CodingAgent()
        return coder.message(message_str, conversations)
        
    def main(self, input_file, conversation_file):
        input_file_path = self.get_workplace_file_path(input_file)
        conversation_file_path = self.get_workplace_file_path(conversation_file)

        conversations, prompt_tokens, completion_tokens = self.read_or_initialize_conversation_file(conversation_file_path)
        message_str = self.process_input_file(input_file_path, conversations)

        response, conversations, prompt_tokens_consumed, completion_tokens_consumed = self.process_message(message_str, conversations)
        
        prompt_tokens += prompt_tokens_consumed
        completion_tokens += completion_tokens_consumed
        self.write_conversations_to_file(conversation_file_path, conversations, prompt_tokens, completion_tokens)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process interactions.")
    parser.add_argument("--input", required=True, help="Input file name")
    parser.add_argument("--conversation", required=True, help="Conversation file name")
    
    args = parser.parse_args()
    agent_runner = CodingAgentRunner()
    agent_runner.main(args.input, args.conversation)