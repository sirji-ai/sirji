import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class TrainUsingSearchTermMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.TRAIN_USING_SEARCH_TERM.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.RESEARCHER.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          TERM: {term}
          """)

    def sample(self):
        return self.generate({
            "term": "The search term that needs to be crawled and trained on."
        })

    def description(self):
        return "Train using a search term:"

    @staticmethod
    def custom_properties():
        return ['TERM']
