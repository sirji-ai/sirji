import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class SolutionCompleteMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.SOLUTION_COMPLETE.name
        self.to_agent = AgentEnum.SIRJI_USER.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            {{solution complete message}}""")})

    def description(self):
        return "Inform that the solution to the problem is complete"

    def instructions(self):
        return []