import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class SearchCodeInProject(BaseMessages):
    def __init__(self):
        self.action = ActionEnum.SEARCH_CODE_IN_PROJECT.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            Search Term: {{Search term}}
            ---""")})

    def description(self):
        return "Search for code in a directory and all its subdirectories"

    def instructions(self):
        return []
