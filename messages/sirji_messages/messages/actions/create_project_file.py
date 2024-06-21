import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class CreateProjectFileMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.CREATE_PROJECT_FILE.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            File path: {{file path}}
            ---
            {{file contents}}""")})

    def description(self):
        return "Create a File Inside Project Folder Only"
    
    def instructions(self):
        return [ "The file path must be relative to the project root.",
                 "The file contents should never be enclosed within ``` starting and ending markers."]

