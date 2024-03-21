import textwrap

from .planner import PlannerPrompt

from .base import PromptGeneratorBase

from sirji.messages.create_file import CreateFileMessage
from sirji.messages.execute_file import ExecuteFileMessage
from sirji.messages.install_package import InstallPackageMessage
from sirji.messages.output import OutputMessage


class ExecutorPrompt(PromptGeneratorBase):

    def __init__(self, caller_name, caller_short_name):
        super().__init__(caller_name, caller_short_name)

    def name(self):
        return "Execution Agent"

    def short_name(self):
        return "Executor"

    def intro_prompt(self):
        return ""  # This will never be called.

    def responsibilities_prompt(self):
        return ""  # This will never be called.

    def capabilities_prompt(self):
        return textwrap.dedent("""
          - Interact with macOS terminal.
          - Create or update files on macOS.
          - Install required dependencies/packages/libraries on macOS.
          - Execute code on macOS.
          """)

    def interact_with(self):
        return [PlannerPrompt(self.name(), self.short_name())]

    def incoming_message_instances(self):
        return [
            CreateFileMessage(self.short_name()),
            ExecuteFileMessage(self.short_name()),
            InstallPackageMessage(self.short_name())
        ]

    def outgoing_message_instances(self):
        return [
            OutputMessage(self.short_name())
        ]

    def ending_prompt(self):
        return ""  # This will never be called.
