import textwrap

from sirji.messages.base import BaseMessages


class InferMessage(BaseMessages):

    def template(self):
        return textwrap.dedent("""
          ```
          FROM: {interactor}
          TO: {implementor}
          ACTION: infer
          DETAILS: {details}
          ```
          """)

    def sample(self, interactor):
        return self.generate(interactor, {
            "details": "Question to extract answers from the trained content."
        })

    def description(self):
        return "Ask questions on the trained content."

    @staticmethod
    def properties():
        return ['FROM', 'TO', 'ACTION', 'DETAILS']
