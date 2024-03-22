import textwrap

from sirji.messages.base import BaseMessages


class CreateFileMessage(BaseMessages):

    def template(self):
        return textwrap.dedent("""
          ```
          FROM: {interactor}
          TO: {implementor}
          ACTION: create-file
          FILENAME: {file_name}
          CONTENT:
          {content}
          ```
          """)

    def sample(self, interactor):
        return self.generate(interactor, {
            "file_name": "File name along with the path.",
            "content": "Multiline file content. It should start from a new line."
        })

    def description(self):
        return "To create a file (with content):"

    @staticmethod
    def properties():
        return ['FROM', 'TO', 'ACTION', 'FILENAME', 'CONTENT']
