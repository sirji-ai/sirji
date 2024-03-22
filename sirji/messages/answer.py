import textwrap

from sirji.messages.base import BaseMessages


class AnswerMessage(BaseMessages):

    def template(self):
        return textwrap.dedent("""
			```
			FROM: {implementor}
			TO: {interactor}
			ACTION: answer
			DETAILS: {details}
			```
			""")

    def sample(self, interactor):
        return self.generate(interactor, {
            "details": "Multiline answer to the asked question."
        })

    def description(self):
        return "The answer to the asked question:"

    @staticmethod
    def properties():
        return ['FROM', 'TO', 'ACTION', 'DETAILS']
