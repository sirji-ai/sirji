import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class ResponseMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.RESPONSE.name
    
        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Agent Id of the agent sending the response}}",
            "to_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "Empty",
            "body": textwrap.dedent("""
            {{Response}}""")})

    def description(self):
        return "The response output"
    
    def instructions(self):
        return []
