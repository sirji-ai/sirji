import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class FetchRecipeIndexMessage(BaseMessages):
    def __init__(self):
        self.action = ActionEnum.FETCH_RECIPE_INDEX.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            EMPTY""")})
    
    def description(self):
        return "Fetch Recipe Index"

    def instructions(self):
        return []