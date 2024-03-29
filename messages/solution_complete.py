import textwrap

from base import BaseMessages

class SolutionCompleteMessage(BaseMessages):

    def template(self):
        return textwrap.dedent("""
          ```
          FROM: {interactor}
          TO: {implementor}
          ACTION: solution-complete
          DETAILS: {details}
          ```
          """)

    def sample(self, interactor):
        return self.generate(interactor, {
            "details": "A concise message to inform that the solution is complete."
        })

    def description(self):
        return "To inform that the solution to the problem is complete:"

    @staticmethod
    def properties():
        return ['FROM', 'TO', 'ACTION', 'DETAILS']
