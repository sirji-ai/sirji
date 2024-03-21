import textwrap

from .base import PromptGeneratorBase

from sirji.messages.infer import Infer
from sirji.messages.train_using_search_term import TrainUsingSearchTerm
from sirji.messages.train_using_url import TrainUsingUrl

from sirji.messages.response import Response
from sirji.messages.output import Output

class Researcher(PromptGeneratorBase):
  def __init__(self, caller_name, caller_short_name):
    super().__init__(caller_name, caller_short_name)

  def name(self):
    return "Research Agent"
  
  def short_name(self):
    return "RA"
  
  def intro_prompt(self):
    return textwrap.dedent("""
      Intro here.
      """)
  
  def responsibilities_prompt(self):
    return textwrap.dedent("""
      Responsibilities here.
      """)
  
  def capabilities_prompt(self):
    return textwrap.dedent("""
      Capabilities here.
      """)  
    
  def ending_prompt(self):
    return textwrap.dedent("""
      Ending here.
      """)
  
  def interact_with(self):
    return []
  
  def incoming_message_instances(self):
    return [TrainUsingSearchTerm(self.short_name()), TrainUsingUrl(self.short_name()), Infer(self.short_name())]

  def outgoing_message_instances(self):
    return [Response(self.short_name()), Output(self.short_name())] 