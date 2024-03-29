import textwrap

from base import BaseMessages

class ResponseMessage(BaseMessages):

    def template(self):
        return textwrap.dedent("""
          ```
          FROM: {implementor}
          TO: {interactor}
          ACTION: response
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
