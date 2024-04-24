import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class ReadFilesMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.READ_FILES.name
        self.from_agent = AgentEnum.CODER.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def template_payload_part(self):
        return textwrap.dedent("""
          FILEPATHS: {file_paths}
          """)

    def sample(self):
        return self.generate({
            "file_paths": "Array of file names along with the path relative to the workspace root folder.",
        })

    def description(self):
        return "To read a file:"

    @staticmethod
    def custom_properties():
        return ['FILEPATHS']
