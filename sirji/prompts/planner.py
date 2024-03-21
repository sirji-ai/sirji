import textwrap

from sirji.messages.problem_statement import ProblemStatement
from sirji.messages.steps import Steps

from .base import PromptGeneratorBase

class Planner(PromptGeneratorBase):
  
  def __init__(self, caller_name, caller_short_name):
    super().__init__(caller_name, caller_short_name)

  def name(self):
    return "Planning Assistant"
  
  def short_name(self):
    return "PA" 
  
  def intro_prompt(self):
    return textwrap.dedent(f"""
      Intro here.
      """)
  
  def responsibilities_prompt(self):
    return textwrap.dedent(f"""
      Job here.
      """)
  
  def capabilities_prompt(self):
    return textwrap.dedent("""
      Capabilities here.
      """)
                           
  def interact_with(self):
    return [] 
  
  def incoming_message_instances(self):
    return [ProblemStatement(self.short_name())]

  def outgoing_message_instances(self):
    return [Steps(self.short_name())]
  
  def ending_prompt(self):
    return ""