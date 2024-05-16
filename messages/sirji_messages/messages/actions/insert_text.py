
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
            FILE_PATH: {{File path}}
            ---
            FIND: {{Text to find}}
            ---
            INSERT_POSITION: {{'above' or 'below'}}
            ---
            TEXT_TO_INSERT: {{Text to insert}}
            ---
            """)})
    
    def description(self):
        return "Insert text into a file at a specific line number"
    
    def instructions(self):
        return []
