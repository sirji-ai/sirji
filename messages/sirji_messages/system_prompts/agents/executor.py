import textwrap

from sirji_messages import AgentEnum

from .planner import PlannerSystemPrompt

from .base import AgentSystemPromptBase


class ExecutorSystemPrompt(AgentSystemPromptBase):

    def name(self):
        return AgentEnum.EXECUTOR.full_name

    def short_name(self):
        return AgentEnum.EXECUTOR.name

    def intro(self):
        return ""  # This will never be called.

    def responsibilities(self):
        return ""  # This will never be called.

    def capabilities(self):
        return textwrap.dedent("""
          - Interact with macOS terminal.
          - Create or update files on macOS.
          - Read content from a single file.
          - Read the content from all files in a directory and all its subdirectories at once (separated by a divider).
          - Install required dependencies/packages/libraries on macOS.
          - Execute code on macOS.
          """)

    def ending_prompt(self):
        return ""  # This will never be called.
