import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class FetchRecipesMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.FETCH_RECIPES.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            Empty""")})

    def description(self):
        return "Fetch Recipe Index"

    def instructions(self):
        return []