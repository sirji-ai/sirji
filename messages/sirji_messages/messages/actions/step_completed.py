import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class StepCompletedMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.STEP_COMPLETED.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.USER.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          DETAILS: {details}
          """)

    def sample(self):
        return self.generate({
            "details": "Example details 'Step # completed'."
        })

    def description(self):
        return "Inform when a step is complete, before moving to the next step:"

    @staticmethod
    def custom_properties():
        return ['DETAILS']
