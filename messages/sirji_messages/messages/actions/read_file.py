import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class ReadFileMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.READ_FILE.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          FILENAME: {file_name}
          """)

    def sample(self):
        return self.generate({
            "file_name": "File name along with the path.",
        })

    def description(self):
        return "To read a file:"

    @staticmethod
    def custom_properties():
        return ['FILENAME']
