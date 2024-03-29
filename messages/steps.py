import textwrap

from base import BaseMessages

class StepsMessage(BaseMessages):

    def template(self):
        return textwrap.dedent("""
          ```
          FROM: {implementor}
          TO: {interactor}
          ACTION: steps
          DETAILS:
          {details}
          ```
          """)

    def sample(self, interactor):
        return self.generate(interactor, {
            "details": "List of steps to solve the problem. Each step is described as 'Step #: ....'."
        })

    def description(self):
        return "List of steps required to solve the problem:"

    @staticmethod
    def properties():
        return ['FROM', 'TO', 'ACTION', 'DETAILS']
