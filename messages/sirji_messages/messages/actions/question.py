import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class QuestionMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.QUESTION.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.USER.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          DETAILS: {details}
          """)

    def sample(self):
        return self.generate({
            "details": "A concise question to understand the problem statement better."
        })

    def description(self):
        return "Ask questions to understand the problem statement better:"

    @staticmethod
    def custom_properties():
        return ['DETAILS']
