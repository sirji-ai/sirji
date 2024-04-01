import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class AnswerMessage(BaseMessages):
    def __init__(self):
        self.action = ActionEnum.ANSWER.name
        self.from_agent = AgentEnum.USER.name
        self.to_agent = AgentEnum.CODER.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          DETAILS: {details}
          """)

    def sample(self):
        return self.generate({
            "details": "Multiline answer to the asked question."
        })

    def description(self):
        return "The answer to the asked question:"

    @staticmethod
    def custom_properties():
        return ['DETAILS']
