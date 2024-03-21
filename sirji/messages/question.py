import textwrap

from sirji.messages.base import BaseMessages 

class QuestionMessage(BaseMessages):
	
	def template(self):
		return textwrap.dedent("""
			```
			FROM: {interactor}
			TO: {implementor}						 
			ACTION: question
			DETAILS: {details}
			```
			""")

	def sample(self,interactor):
		return self.generate(interactor, {
			"details": "A concise question to understand the problem statement better."
        })
	
	def description(self):
		return "Ask questions to understand the problem statement better:"    