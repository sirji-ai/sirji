from .base import AgentRunnerBase
from sirji_agents import PlanningAgent
import argparse

class PlanningAgentRunner(AgentRunnerBase):
    def process_input_file(self, input_file_path, conversations):
        with open(input_file_path, 'r') as file:
            contents = file.read()
        return contents

    def process_message(self, message_str, conversations):
        planner = PlanningAgent()
        return planner.message(message_str, conversations)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process interactions.")
    parser.add_argument("--input", required=True, help="Input file name")
    parser.add_argument("--conversation", required=True, help="Conversation file name")
    
    args = parser.parse_args()
    agent_runner = PlanningAgentRunner()
    agent_runner.main(args.input, args.conversation)