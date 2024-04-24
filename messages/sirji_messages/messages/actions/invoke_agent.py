import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class InvokeAgentMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.INVOKE_AGENT.name
        self.from_agent = AgentEnum.ORCHESTRATOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "to_agent_id": "{{Installed Agent ID}}",
            "summary": "{{A concise summary to be displayed to the user for the action to be performed.}}",
            "body": textwrap.dedent("""
            {{Purpose of invocation}}
            """)})

    def description(self):
        return "To invoke an installed agent:"
