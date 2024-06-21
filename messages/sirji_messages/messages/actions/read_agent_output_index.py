import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class ReadAgentOutputIndexMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.READ_AGENT_OUTPUT_INDEX.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            Empty""")})

    def description(self):
        return "Read Agent Output Index"

    def instructions(self):
        return []