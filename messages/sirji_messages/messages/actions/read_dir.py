import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class ReadDirMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.READ_DIR.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          DIRPATH: {dir_path}
          """)

    def sample(self):
        return self.generate({
            "dir_path": "Name of a directory alongwith the path.",
        })

    def description(self):
        return "To read the content from all files in a directory and all its subdirectories at once (separated by a divider):"

    @staticmethod
    def custom_properties():
        return ['DIRPATH']
