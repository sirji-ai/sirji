import textwrap

from sirji.messages.base import BaseMessages 

class StepStarted(BaseMessages):
	
	def template(self):
		return textwrap.dedent("""
			```
			FROM: {interactor}
			TO: {implementor}
			ACTION: step-started
			DETAILS: {details}
			```
			""")

	def sample(self,interactor):
		return self.generate(interactor, {
			"details": "Example details 'Step # started'."
        })
	
	def description(self):
		return "Inform the step you are about to start on:"    