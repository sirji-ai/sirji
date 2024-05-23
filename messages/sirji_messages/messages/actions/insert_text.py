
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
            FIND: 
            {{Code to Find}}
            ---
            CODE_TO_INSERT: 
            {{Code to insert}}
            ---
            INSERT_POSITION_RELATIVE_TO_FIND:
            {{above or below}}
            ---
            """)})
    
    def description(self):
        return "Insert text into a file at a specific line number"
    
    def instructions(self):
        return [
            "The FILE_PATH must be a valid path to the file where you want to insert the code. Ensure that the file path is correct and that the file exists. If the file does not exist, the action will fail.",
            "The FIND must be a valid, uniquely identifiable code in the file. Ensure that you provide the FIND considering that new code will be inserted above or below this code. After insertion, it should not disturb the scope of the existing code in the file or create any syntax errors."
            "The CODE_TO_INSERT must be a valid code that you want to insert into the file. Ensure that the code is correctly formatted and does not create any syntax errors in the file."
            "The INSERT_POSITION_RELATIVE_TO_FIND must be either above or below. If you want to insert the code above the FIND, provide above. If you want to insert the code below the FIND, provide below. We will use this as follows: if above, we will replace the FIND with (CODE_TO_INSERT)(FIND); if below, we will replace the FIND with (FIND)(CODE_TO_INSERT). Please make sure that the code is correctly formatted and does not create any syntax errors in the file."
            "For all the keys present in the BODY, make sure you don't enclose them in any special characters. Just provide the values."
            "Make sure the CODE_TO_INSERT is correctly formatted and has the proper indentation in place. If the indentation is not correct, it may create syntax errors in the file."
        ]
