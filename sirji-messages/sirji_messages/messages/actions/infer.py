import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class InferMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.INFER.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.RESEARCHER.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          DETAILS: {details}
          """)

    def sample(self):
        return self.generate({
            "details": "Question to extract answers, code examples, GitHub URLs, relevant external URLs from the trained content."
        })

    def description(self):
        return "Ask questions on the trained content:"

    @staticmethod
    def custom_properties():
        return ['DETAILS']
