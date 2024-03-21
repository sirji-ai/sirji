import textwrap

from .planner import PlannerPrompt
from .researcher import ResearcherPrompt
from .executor import ExecutorPrompt
from .user import UserPrompt

from .base import PromptGeneratorBase

class CoderPrompt(PromptGeneratorBase):
  
  def __init__(self):
    super().__init__(None, None)

  def name(self):
    return "Coder"
  
  def short_name(self):
    return "CR" 
  
  def intro_prompt(self):
    return textwrap.dedent(f"""
      Intro here.
      """)
  
  def responsibilities_prompt(self):
    return textwrap.dedent(f"""
      Responsibilities here.
      """)
  
  def capabilities_prompt(self):
    return textwrap.dedent("""
      Capabilities here.
      """)
                           
  def interact_with(self):
    return [
      PlannerPrompt(self.name(), self.short_name()),
      ResearcherPrompt(self.name(), self.short_name()),
      ExecutorPrompt(self.name(), self.short_name()),
      UserPrompt(self.name(), self.short_name())
      ] 
  
  def incoming_message_instances(self):
    return []

  def outgoing_message_instances(self):
    return []
  
  def ending_prompt(self):
    return ""