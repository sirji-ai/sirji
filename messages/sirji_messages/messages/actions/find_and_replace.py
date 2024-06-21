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
              "step": "Provide the step number here for the ongoing step if any.",
              "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
              "body": textwrap.dedent("""
                FILE_PATH:
                {{File path}}                        
                --- 
                FIND:
                {{Code to Find}}    
                ---                   
                REPLACE:
                {{Code to Replace}}
                ---
            """)})
  
      def description(self):
          return "Find and Replace code in a file"
  
      def instructions(self):
          return [
            "The FILE_PATH must be a valid path to the file where you want to insert the code. Ensure that the file path is correct and that the file exists. If the file does not exist, the action will fail.",
            "The FIND must be a valid, uniquely identifiable code in the file"
            "The REPLACE must be a valid code that you want to replace with FIND into the file. Ensure that the code is correctly formatted and does not create any syntax errors in the file."
            "For all the keys present in the BODY, make sure you don't enclose them in any special characters. Just provide the values."
            "Make sure the REPLACE is correctly formatted and has the proper indentation in place. If the indentation is not correct, it may create syntax errors in the file."
          ]