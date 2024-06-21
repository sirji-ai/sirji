import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class FetchRecipeMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.FETCH_RECIPE.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            File path: {{File path}}""")})
    
    def description(self):
        return "Fetch Recipe"

    def instructions(self):
        return [ "The body must be in the following format: File path: file_path"]