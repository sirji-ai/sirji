import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class ReadDirStructureMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.READ_DIR_STRUCTURE.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            Directory: {{Directory path}}""")})

    def description(self):
        return "Read the structure of a directory"
    
    def instructions(self):
        return []