import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class ExecuteCommandMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.EXECUTE_COMMAND.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          COMMAND: {command}
          """)

    def sample(self):
        return self.generate({
            "command": "Command to execute."
        })

    def description(self):
        return "To execute a command:"

    @staticmethod
    def custom_properties():
        return ['COMMAND']
