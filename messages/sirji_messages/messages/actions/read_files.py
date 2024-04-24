import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class ReadFilesMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.READ_FILES.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "summary": "{{A concise summary to be displayed to the user for the action to be performed.}}",
            "body": textwrap.dedent("""
            File paths: {{Array of file paths}}
            """)})
    
    def description(self):
        return "To read files:"
