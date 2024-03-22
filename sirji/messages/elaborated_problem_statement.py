import textwrap

from sirji.messages.base import BaseMessages


class ElaboratedProblemStatementMessage(BaseMessages):

    def template(self):
        return textwrap.dedent("""
          ```
          FROM: {interactor}
          TO: {implementor}
          ACTION: elaborated-problem-statement
          DETAILS: {details}
          ```
          """)

    def sample(self, interactor):
        return self.generate(interactor, {
            "details": "Problem statement (PS) here."
        })

    def description(self):
        return "Generate steps for the problem statement (PS):"

    @staticmethod
    def properties():
        return ['FROM', 'TO', 'ACTION', 'DETAILS']
