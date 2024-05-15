import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class AppendToAgentOutputIndexMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.APPEND_TO_AGENT_OUTPUT_INDEX.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            File path: {{file path of the agent output file relative to the Agent Output Folder}}
            ---
            {{Description of the agent output file, to be used by other agents to know what it is about}}""")})

    def description(self):
        return "Register to the Agent Output Index"
    
    def instructions(self):
        return [ "Ensure to register new agent output files to the Agent Output Index.",
                 "The file path must be in the following format: '{{Your Agent ID}}/{{file name}}'."]
