import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class AcknowledgeMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.ACKNOWLEDGE.name
        self.from_agent = AgentEnum.USER.name
        self.to_agent = AgentEnum.CODER.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
            DETAILS: Sure.
            """)

    def sample(self):
        return self.generate({})

    def description(self):
        return "The message acknowledgment:"

    @staticmethod
    def custom_properties():
        return ['DETAILS']
