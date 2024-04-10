import textwrap

from sirji_messages import AgentEnum, ActionEnum

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
          - Run server process using {ActionEnum.RUN_SERVER.name} action.
          - Create or update files using {ActionEnum.CREATE_FILE.name} action.
          - Read content from a single file using {ActionEnum.READ_FILE.name} action.
          - Read the content from all files in a directory and all its subdirectories at once (separated by a divider) using {ActionEnum.READ_DIR.name} action.
          - Install required dependencies/packages/libraries using {ActionEnum.INSTALL_PACKAGE.name} action.
          - Execute code and command using {ActionEnum.EXECUTE_COMMAND.name} action.
          """)

    def ending_prompt(self):
        return ""  # This will never be called.
