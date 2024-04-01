import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class ResponseMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.RESPONSE.name
        self.from_agent = AgentEnum.RESEARCHER.name
        self.to_agent = AgentEnum.CODER.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          DETAILS:
          {details}
          """)

    def sample(self):
        return self.generate({
            "details": "Multilined response."
        })

    def description(self):
        return "The response output:"

    @staticmethod
    def custom_properties():
        return ['DETAILS']
