import textwrap

from sirji.messages.base import BaseMessages 

class InstallPackage(BaseMessages):
	
	def template(self):
		return textwrap.dedent("""
			```
			FROM: {interactor}
			TO: {implementor}
			ACTION: install-package
			COMMAND: {command}							 
			```
			""")

	def sample(self,interactor):
		return self.generate(interactor, {
			"command": "Command to install the package or library."
        })
	
	def description(self):
		return "To install a package or library:"