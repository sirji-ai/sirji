import textwrap

from sirji.messages.base import BaseMessages


class OutputMessage(BaseMessages):

    def template(self):
        return textwrap.dedent("""
          ```
          FROM: {implementor}
          TO: {interactor}
          ACTION: output
          DETAILS:
          {details}
          ```
          """)

    def sample(self, interactor):
        return self.generate(interactor, {
            "details": "Multilined response."
        })

    def description(self):
        return "The response output:"

    @staticmethod
    def properties():
        return ['FROM', 'TO', 'ACTION', 'DETAILS']
