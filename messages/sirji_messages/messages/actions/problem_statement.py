import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class ProblemStatementMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.PROBLEM_STATEMENT.name
        self.from_agent = AgentEnum.USER.name
        self.to_agent = AgentEnum.CODER.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          DETAILS: {details}
          """)

    def sample(self):
        return self.generate({
            "details": "The problem statement (PS) that needs to be solved programmatically."
        })

    def description(self):
        return "The problem statement (PS) that needs to be solved programmatically:"

    @staticmethod
    def custom_properties():
        return ['DETAILS']
