import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class ReadDirStructureMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.READ_DIR_STRUCTURE.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          DIRPATH: {dir_path}
          """)

    def sample(self):
        return self.generate({
            "dir_path": "Name of a directory along with the path relative to the workspace root folder.",
        })

    def description(self):
        return "To read the structure of a directory."

    @staticmethod
    def custom_properties():
        return ['DIRPATH']
