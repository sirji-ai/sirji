import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class InvokeAgentExistingSessionMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.INVOKE_AGENT_EXISTING_SESSION.name
        self.from_agent = AgentEnum.ORCHESTRATOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "to_agent_id": "{{To Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            {{Purpose of invocation}}""")})

    def description(self):
        return "Invoke an agent continuing on the existing session"
    
    def instructions(self):
        return [
            "Never use this action while invoking an agent for the first time."
        ]
