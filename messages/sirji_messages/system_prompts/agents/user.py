import textwrap

from sirji_messages import AgentEnum

from .planner import PlannerSystemPrompt

from .base import AgentSystemPromptBase


class UserSystemPrompt(AgentSystemPromptBase):

    def name(self):
        return AgentEnum.SIRJI_USER.full_name

    def short_name(self):
        return AgentEnum.SIRJI_USER.name

    def intro(self):
        return ""  # This will never be called.

    def responsibilities(self):
        return ""  # This will never be called.

    def capabilities(self):
        return textwrap.dedent("""
          - Provide the problem statement (PS).   
          - Provide the answer to the question asked.             
          - Acknowledge started or completed steps.
          - Acknowledge the final solution.
          """)

    def ending_prompt(self):
        return ""  # This will never be called.
