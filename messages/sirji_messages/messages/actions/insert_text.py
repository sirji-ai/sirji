
import textwrap;
from sirji_messages import AgentEnum, ActionEnum;

from .base import BaseMessages;

class InsertText(BaseMessages):
    
    def __init__(self):
        self.action = ActionEnum.INSERT_TEXT.name
        self.to_agent = AgentEnum.EXECUTOR.name
        
        super().__init__()
    
    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            FILE_PATH: 
            {{File path}}
            ---
            FIND_CODE: 
            {{code to be found in the file}}
            ---
            INSERT_DIRECTION:
            {{The direction to insert the code relative to the found code; can be either above or below.}}
            ---
            CODE_TO_INSERT: 
            {{Code to be inserted in the file}}
            ---
            """)})
    
    def description(self):
        return "Insert text into a file at a specific location relative to a given code snippet."

    def instructions(self):
        return [
            "File path must be relative to the project root. This action cannot create new files and will fail if the file doesn't exist.",
            "Code to be found must be a valid, uniquely identifiable piece of code within the relevant scope. Ensure it allows proper insertion without causing syntax errors",
            "Insert direction must be ‘above’ or ‘below’. It specifies where to insert CODE_TO_INSERT relative to FIND_CODE. Incorrect values will disrupt functionality. If 'above', CODE_TO_INSERT will be inserted before FIND_CODE; if 'below', it will be inserted after.",
            "CODE_TO_INSERT must be valid and correctly formatted code to be inserted. Ensure it does not cause syntax errors and has proper indentation.",
            "When providing values for the keys in the BODY, do not enclose them in special characters.",
        ]
