import textwrap

from sirji.messages.base import BaseMessages 

class StepsMessage(BaseMessages):
	
	def template(self):
		return textwrap.dedent("""
			```
			FROM: {implementor}
			TO: {interactor}
			ACTION: steps
			SUMMARY: {summary}
			DETAILS: {details}
			```
			""")

	def sample(self,interactor):
		return self.generate(interactor, {
            "summary": "summarize your understanding of the problem statement",
            "details": "Multiline details of steps to solve the problem. Each step is described as 'Step #: ....'. Don't explain the steps using multiple sub-step points."
        })
	
	def description(self):
		return "List of steps required to solve the problem:"   

	def properties(self):
		return ['FROM', 'TO', 'ACTION', 'SUMMARY', 'DETAILS'] 