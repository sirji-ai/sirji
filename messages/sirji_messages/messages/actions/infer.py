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
            "summary": "{{A concise summary to be displayed to the user for the action to be performed.}}",
            "body": textwrap.dedent("""
            {{Infer query}}
            """)})

    def description(self):
        return "Ask questions on the trained content:"
