import textwrap

from sirji.messages.base import BaseMessages 

class ExecuteFileMessage(BaseMessages):
	
	def template(self):
		return textwrap.dedent("""
			```
			FROM: {interactor}
			TO: {implementor}
			ACTION: execute-file
			COMMAND: {command}							 
			```
			""")

	def sample(self,interactor):
		return self.generate(interactor, {
			"command": "Command to execute a file."
        })
	
	def description(self):
		return "To execute a file:"