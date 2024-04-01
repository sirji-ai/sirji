import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class SolutionCompleteMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.SOLUTION_COMPLETE.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.USER.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          DETAILS: {details}
          """)

    def sample(self):
        return self.generate({
            "details": "A concise message to inform that the solution is complete."
        })

    def description(self):
        return "To inform that the solution to the problem is complete:"

    @staticmethod
    def custom_properties():
        return ['DETAILS']
