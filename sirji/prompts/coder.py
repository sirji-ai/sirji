import textwrap

from .planner import Planner
from .researcher import Researcher
from .executor import Executor
from .user import User

from .base import PromptGeneratorBase

class Coder(PromptGeneratorBase):
  
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
      Planner(self.name(), self.short_name()),
      Researcher(self.name(), self.short_name()),
      Executor(self.name(), self.short_name()),
      User(self.name(), self.short_name())
      ] 
  
  def incoming_message_instances(self):
    return []

  def outgoing_message_instances(self):
    return []
  
  def ending_prompt(self):
    return ""