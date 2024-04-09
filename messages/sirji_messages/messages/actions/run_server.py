import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class RunServerMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.RUN_SERVER.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          COMMAND: {command}
          """)

    def sample(self):
        return self.generate({
            "command": "Command to start server process."
        })

    def description(self):
        return "To start server process:"

    @staticmethod
    def custom_properties():
        return ['COMMAND']
