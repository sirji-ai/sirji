import textwrap

from sirji.messages.base import BaseMessages 

class ProblemStatementMessage(BaseMessages):
	
	def template(self):
		return textwrap.dedent("""
			```
			FROM: {interactor}
			TO: {implementor}
			ACTION: problem-statement
			DETAILS: {details}
			```
			""")

	def sample(self,interactor):
		return self.generate(interactor, {
			"details": "The problem statement (PS) that needs to be solved programmatically."
        })
	
	def description(self):
		return "The problem statement (PS) that needs to be solved programmatically:"