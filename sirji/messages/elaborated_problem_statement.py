import textwrap

from sirji.messages.base import BaseMessages


class ElaboratedProblemStatementMessage(BaseMessages):

    def template(self):
        return textwrap.dedent("""
          ```
          FROM: {interactor}
          TO: {implementor}
          ACTION: problem-statement
          DETAILS: {details}
          ```
          """)

    def sample(self, interactor):
        return self.generate(interactor, {
            "details": "Elaborated/rephrased problem statement (PS) for which the steps need to be generated."
        })

    def description(self):
        return "Generate steps for the elaborated/rephrased problem statement (PS):"

    @staticmethod
    def properties():
        return ['FROM', 'TO', 'ACTION', 'DETAILS']
