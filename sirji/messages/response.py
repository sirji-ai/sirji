import textwrap

from sirji.messages.base import BaseMessages 

class ResponseMessage(BaseMessages):
	
	def template(self):
		return textwrap.dedent("""
			```
			FROM: {implementor}
			TO: {interactor}
			ACTION: response
			DETAILS: {details}
			```
			""")

	def sample(self,interactor):
		return self.generate(interactor, {
			"details": "Multiline details of the response received after execution."
        })
	
	def description(self):
		return "The response output:"