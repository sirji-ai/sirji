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
            "summary": "{{A concise summary to be displayed to the user for the action to be performed.}}",
            "body": textwrap.dedent("""
            {{solution complete message}}
            """)})

    def description(self):
        return "To inform that the solution to the problem is complete:"