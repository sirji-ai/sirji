
import textwrap;
from sirji_messages import AgentEnum, ActionEnum;

from .base import BaseMessages;

class InsertBelow(BaseMessages):
    
    def __init__(self):
        self.action = ActionEnum.INSERT_BELOW.name
        self.to_agent = AgentEnum.EXECUTOR.name
        
        super().__init__()
    
    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            FILE_PATH: 
            {{File path}}
            ---
            NEW_CHANGES: 
            {{New code to be inserted in the file}}
            ---
            INSERT_BELOW: 
            {{Provide few lines of code below which the new code needs to be inserted.}}
            ---
            """)})
    
    def description(self):
        return "Immediately insert new code below a specific piece of code in a file."

    def instructions(self):
        return [
            "File path must be relative to the project root. This action cannot create new files and will fail if the file doesn't exist.",
            "NEW_CHANGES must be valid and correctly formatted code to be inserted. Ensure it does not cause syntax errors and has proper indentation.",
            "INSERT_BELOW must be a valid, uniquely identifiable piece of code within the relevant scope. Ensure it is a valid insertion point without causing syntax errors",
            "When providing values for the keys in the BODY, do not enclose them in special characters.",
            "Ensure that the INSERT_BELOW code snippet has the same indentation as the existing code in the file. The indentation must match exactly to avoid leaving a comma, semicolon, or any other character that could cause syntax errors. Carefully check the number of spaces or tabs used in the existing code and replicate it precisely in the INSERT_BELOW snippet."
        ]
