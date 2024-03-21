import textwrap

from sirji.messages.base import BaseMessages 

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

	def sample(self,interactor):
		return self.generate(interactor, {
			"details": "A concise message to inform that the solution is complete and if any further help is needed."
        })
	
	def description(self):
		return "To inform that the solution to the problem is complete:"    