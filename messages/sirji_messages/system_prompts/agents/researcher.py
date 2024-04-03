import textwrap

from sirji_messages import AgentEnum

from .base import AgentSystemPromptBase


class ResearcherSystemPrompt(AgentSystemPromptBase):

    def name(self):
        return AgentEnum.RESEARCHER.full_name

    def short_name(self):
        return AgentEnum.RESEARCHER.name

    def intro(self):
        return ""  # This will never be called.

    def responsibilities(self):
        return ""  # This will never be called.

    def capabilities(self):
        return textwrap.dedent("""
            - Crawl the given URL and get trained on its content.
            - Infer from the trained content/knowledge and try to respond to questions asked.
            """)

    def ending_prompt(self):
        return ""  # This will never be called.
