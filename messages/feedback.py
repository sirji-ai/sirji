import textwrap

from base import BaseMessages

class FeedbackMessage(BaseMessages):

    def template(self):
        return textwrap.dedent("""
          ```
          FROM: {implementor}
          TO: {interactor}
          ACTION: feedback
          DETAILS: {details}
          ```
          """)

    def sample(self, interactor):
        return self.generate(interactor, {
            "details": "Feedback on the solution provided."
        })

    def description(self):
        return "Feedback on the solution provided:"

    @staticmethod
    def properties():
        return ['FROM', 'TO', 'ACTION', 'DETAILS']
