import textwrap

from sirji.messages.base import BaseMessages 

class ElaboratedProblemStatement(BaseMessages):
	
	def template(self):
		return textwrap.dedent("""
			```
			FROM: {implementor}
			TO: {interactor}
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