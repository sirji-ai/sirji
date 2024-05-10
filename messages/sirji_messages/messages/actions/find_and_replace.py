import textwrap

from sirji_messages import AgentEnum, ActionEnum

from .base import BaseMessages

class FindAndReplace(BaseMessages):
  
      def __init__(self):
          self.action = ActionEnum.FIND_AND_REPLACE.name
          self.to_agent = AgentEnum.EXECUTOR.name
  
          super().__init__()
  
      def sample(self):
          return self.generate({
              "from_agent_id": "{{Your Agent ID}}",
              "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
              "body": textwrap.dedent("""
                FILE_PATH: {{File path}}                        
                --- 
                FIND: {{Find this text}}    
                ---                   
                REPLACE: {{Replace with this text}}
                ---
            """)})
  
      def description(self):
          return "Find and Replace text in a file"
  
      def instructions(self):
          return []