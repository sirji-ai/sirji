import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages

class CreateAgentOutputFileMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.CREATE_AGENT_OUTPUT_FILE.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "summary": "{{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            File path: {{file path}}
            ---
            {{file contents}}""")})

    def description(self):
        return "Create a File Inside Agent Output Folder"
    
    def instructions(self):
        return [ "The file path must be in the following format: '{{Your Agent ID}}/{{file name}}'."]

