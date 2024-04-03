from .base import AgentRunnerBase
from sirji_messages import MessageFactory, ActionEnum
from sirji_agents import CodingAgent
import argparse

class CodingAgentRunner(AgentRunnerBase):
    def process_input_file(self, input_file_path, conversations):
        with open(input_file_path, 'r') as file:
            contents = file.read()

        if not conversations:
            message_class = MessageFactory[ActionEnum.PROBLEM_STATEMENT.name]
            message_str = message_class().generate({"details": contents})
        else:
            message_str = contents
        
        return message_str

    def process_message(self, message_str, conversations):
        coder = CodingAgent()
        return coder.message(message_str, conversations)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process interactions.")
    parser.add_argument("--input", required=True, help="Input file name")
    parser.add_argument("--conversation", required=True, help="Conversation file name")
    
    args = parser.parse_args()
    agent_runner = CodingAgentRunner()
    agent_runner.main(args.input, args.conversation)