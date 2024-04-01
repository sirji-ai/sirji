import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class TrainUsingUrlMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.TRAIN_USING_URL.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.RESEARCHER.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          URL: {url}
          """)

    def sample(self):
        return self.generate({
            "url": "The URL that needs to be crawled, parsed, and trained to answer questions."
        })

    def description(self):
        return "Train using a URL:"

    @staticmethod
    def custom_properties():
        return ['URL']
