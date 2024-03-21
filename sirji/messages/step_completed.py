import textwrap

from sirji.messages.base import BaseMessages 

class StepCompletedMessage(BaseMessages):
	
	def template(self):
		return textwrap.dedent("""
			```
			FROM: {interactor}
			TO: {implementor}
			ACTION: step-completed
			DETAILS: {details}
			```
			""")

	def sample(self,interactor):
		return self.generate(interactor, {
			"details": "Example details 'Step # completed'."
        })
	
	def description(self):
		return "Inform when a step is complete, before moving to the next step:"    