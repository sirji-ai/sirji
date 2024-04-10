import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class InstallPackageMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.INSTALL_PACKAGE.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          COMMAND: {command}
          """)

    def sample(self):
        return self.generate({
            "command": "Command to install the package or library."
        })

    def description(self):
        return "To install a package or library:"

    @staticmethod
    def custom_properties():
        return ['COMMAND']
