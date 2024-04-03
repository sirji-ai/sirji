import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class StepStartedMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.STEP_STARTED.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.USER.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          DETAILS: {details}
          """)

    def sample(self):
        return self.generate({
            "details": "Example details 'Step # started'."
        })

    def description(self):
        return "Inform the step you are about to start on:"

    @staticmethod
    def custom_properties():
        return ['DETAILS']
