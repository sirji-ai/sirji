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
            "summary": "{{A concise summary to be displayed to the user for the action to be performed.}}",
            "body": textwrap.dedent("""
            Directory: {{Directory path}}
            """)})

    def description(self):
        return "To read the structure of a directory."