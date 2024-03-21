import textwrap

from sirji.messages.base import BaseMessages 

class AcknowledgeMessage(BaseMessages):
	
	def template(self):
		return textwrap.dedent("""
			```
			FROM: {implementor}
			TO: {interactor}
			ACTION: acknowledge
			DETAILS: Sure.
			```
			""")

	def sample(self,interactor):
		return self.generate(interactor, {})
	
	def description(self):
		return "The message acknowledgement:"