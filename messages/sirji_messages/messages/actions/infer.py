import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class InferMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.INFER.name
        self.to_agent = AgentEnum.RESEARCHER.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            {{query}}""")})

    def description(self):
        return "Ask questions on the trained content"
    
    def instructions(self):
        return []
