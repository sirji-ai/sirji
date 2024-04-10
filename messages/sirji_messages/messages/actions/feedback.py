import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class FeedbackMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.FEEDBACK.name
        self.from_agent = AgentEnum.USER.name
        self.to_agent = AgentEnum.CODER.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          DETAILS: {details}
          """)

    def sample(self):
        return self.generate({
            "details": "Feedback on the solution provided."
        })

    def description(self):
        return "Feedback on the solution provided:"

    @staticmethod
    def custom_properties():
        return ['DETAILS']
