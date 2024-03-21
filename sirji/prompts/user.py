import textwrap

from .planner import PlannerPrompt

from .base import PromptGeneratorBase

from sirji.messages.elaborated_problem_statement import ElaboratedProblemStatement
from sirji.messages.answer import Answer
from sirji.messages.acknowledge import Acknowledge
from sirji.messages.question import Question
from sirji.messages.step_completed import StepCompleted
from sirji.messages.step_started import StepStarted
from sirji.messages.solution_complete import SolutionComplete

class UserPrompt(PromptGeneratorBase):
  
  def __init__(self, caller_name, caller_short_name):
    super().__init__(caller_name, caller_short_name)

  def name(self):
    return "User"
  
  def short_name(self):
    return "UR"
  
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
      Question(self.short_name()),
      StepCompleted(self.short_name()), 
      StepStarted(self.short_name()), 
      SolutionComplete(self.short_name())
      ]

  def outgoing_message_instances(self):
    return [
      ElaboratedProblemStatement(self.short_name()), 
      Answer(self.short_name()), 
      Acknowledge(self.short_name())
    ]
  
  def ending_prompt(self):
    return ""