import textwrap

from .planner import PlannerPrompt

from .base import PromptGeneratorBase

from sirji.messages.elaborated_problem_statement import ElaboratedProblemStatementMessage
from sirji.messages.answer import AnswerMessage
from sirji.messages.acknowledge import AcknowledgeMessage
from sirji.messages.question import QuestionMessage
from sirji.messages.step_completed import StepCompletedMessage
from sirji.messages.step_started import StepStartedMessage
from sirji.messages.solution_complete import SolutionCompleteMessage

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
      QuestionMessage(self.short_name()),
      StepCompletedMessage(self.short_name()), 
      StepStartedMessage(self.short_name()), 
      SolutionCompleteMessage(self.short_name())
      ]

  def outgoing_message_instances(self):
    return [
      ElaboratedProblemStatementMessage(self.short_name()), 
      AnswerMessage(self.short_name()), 
      AcknowledgeMessage(self.short_name())
    ]
  
  def ending_prompt(self):
    return ""