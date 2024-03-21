import textwrap

from sirji.messages.base import BaseMessages 

class CreateFileMessage(BaseMessages):
	
	def template(self):
		return textwrap.dedent("""
			```
			FROM: {interactor}
			TO: {implementor}
			SUBJECT: create-file
			FILENAME: {file_name}									 
			CONTENT: {content}
			```
			""")

	def sample(self,interactor):
		return self.generate(interactor, {
			"file_name": "Name of the file to create",
			"content": "Multiline file content here."
        })
	
	def description(self):
		return "To create a file (with content):"