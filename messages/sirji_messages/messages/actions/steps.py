import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class StepsMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.STEPS.name
        self.from_agent = AgentEnum.PLANNER.name
        self.to_agent = AgentEnum.CODER.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          DETAILS:
          {details}
          """)

    def sample(self):
        return self.generate({
            "details": "List of steps to solve the problem. Each step must start with 'Step #: ....'."
        })

    def description(self):
        return "List of steps required to solve the problem:"

    @staticmethod
    def custom_properties():
        return ['DETAILS']