import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages

class CreateAssistantMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.CREATE_ASSISTANT.name
        self.to_agent = AgentEnum.RESEARCHER.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            Provide the instructions to create the assistant here.
            """)
        })
    
    def description(self):
        return "Create Assistant"

    def instructions(self):
        return []