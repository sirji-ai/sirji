import textwrap

from .base import PromptGeneratorBase

from sirji.messages.infer import InferMessage
from sirji.messages.train_using_search_term import TrainUsingSearchTermMessage
from sirji.messages.train_using_url import TrainUsingUrlMessage

from sirji.messages.response import ResponseMessage
from sirji.messages.output import OutputMessage


class ResearcherPrompt(PromptGeneratorBase):
    def __init__(self, caller_name, caller_short_name):
        super().__init__(caller_name, caller_short_name)

    def name(self):
        return "Research Agent"

    def short_name(self):
        return "Researcher"

    def intro_prompt(self):
        return ""  # This will never be called.

    def responsibilities_prompt(self):
        return ""  # This will never be called.

    def capabilities_prompt(self):
        return textwrap.dedent("""
          - Crawl given URL and get trained on it's content.
          - Seach for a term and crawl first few result URLs to get trained on their content.
          - Infer from the trained content/knowledge and try to respond to questions asked.
          """)

    def ending_prompt(self):
        return ""  # This will never be called.

    def interact_with(self):
        return []

    def incoming_message_instances(self):
        return [TrainUsingSearchTermMessage(self.short_name()), TrainUsingUrlMessage(self.short_name()), InferMessage(self.short_name())]

    def outgoing_message_instances(self):
        return [ResponseMessage(self.short_name()), OutputMessage(self.short_name())]
