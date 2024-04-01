import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class GenerateStepsMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.GENERATE_STEPS.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.PLANNER.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          DETAILS: {details}
          """)

    def sample(self):
        return self.generate({
            "details": "Problem statement (PS) here."
        })

    def description(self):
        return "Generate steps for the problem statement (PS):"

    @staticmethod
    def custom_properties():
        return ['DETAILS']
