import textwrap

from sirji.messages.base import BaseMessages 

class InferMessage(BaseMessages):
	
	def template(self):
		return textwrap.dedent("""
			```
			FROM: {interactor}
			TO: {implementor}
			ACTION: infer
			DETAILS: {details}
			```
			""")

	def sample(self,interactor):
		return self.generate(interactor, {
			"details": "Question to extract answers from the trained data."
        })
	
	def description(self):
		return "Ask questions to RA on the trained data:"    
	
	def properties(self):
		return ['FROM', 'TO', 'ACTION', 'DETAILS']