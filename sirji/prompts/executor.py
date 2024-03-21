import textwrap

from .planner import PlannerPrompt

from .base import PromptGeneratorBase

from sirji.messages.create_file import CreateFile
from sirji.messages.execute_file import ExecuteFile
from sirji.messages.install_package import InstallPackage
from sirji.messages.output import Output

class ExecutorPrompt(PromptGeneratorBase):
  
  def __init__(self, caller_name, caller_short_name):
    super().__init__(caller_name, caller_short_name)

  def name(self):
    return "Executor"
  
  def short_name(self):
    return "ER"
  
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
    return [PlannerPrompt(self.name(), self.short_name())] 
  
  def incoming_message_instances(self):
    return [
      CreateFile(self.short_name()),
      ExecuteFile(self.short_name()), 
      InstallPackage(self.short_name())
    ]

  def outgoing_message_instances(self):
    return [
      Output(self.short_name())
    ]
  
  def ending_prompt(self):
    return ""