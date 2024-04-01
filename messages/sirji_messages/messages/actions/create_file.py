import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class CreateFileMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.CREATE_FILE.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          FILENAME: {file_name}
          CONTENT:
          {content}
          """)

    def sample(self):
        return self.generate({
            "file_name": "File name along with the path.",
            "content": "Multiline file content. It should start from a new line."
        })

    def description(self):
        return "To create a file (with content):"

    @staticmethod
    def custom_properties():
        return ['FILENAME', 'CONTENT']
