import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class InformMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.INFORM.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.USER.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          DETAILS: {details}
          """)

    def sample(self):
        return self.generate({
            "details": "Details of your decisions or choices."
        })

    def description(self):
        return "To inform about your decisions or choices:"

    @staticmethod
    def custom_properties():
        return ['DETAILS']
