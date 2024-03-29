import textwrap
from base import BaseMessages

class AcknowledgeMessage(BaseMessages):

    def template(self):
        return textwrap.dedent("""
            ```
            FROM: {implementor}
            TO: {interactor}
            ACTION: acknowledge
            DETAILS: Sure.
            ```
            """)

    def sample(self, interactor):
        return self.generate(interactor, {})

    def description(self):
        return "The message acknowledgment:"

    @staticmethod
    def properties():
        return ['FROM', 'TO', 'ACTION', 'DETAILS']
