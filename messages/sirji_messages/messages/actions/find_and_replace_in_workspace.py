import textwrap
from sirji_messages import AgentEnum, ActionEnum

from .base import BaseMessages

class FindAndReplaceInWorkspaceMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.FIND_AND_REPLACE_IN_WORKSPACE.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            Find: {{Find this text}}
            ---                        
            Replace: {{Replace with this text}}
            ---
            Directory: {{Directory path}}""")})

    def description(self):
        return "Find and Replace text in all files in a directory and all its subdirectories"

    def instructions(self):
        return []