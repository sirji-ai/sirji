import textwrap;

from sirji_messages import AgentEnum, ActionEnum;
from .base import BaseMessages;

class SyncCodebase(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.SYNC_CODEBASE.name
        self.to_agent = AgentEnum.RESEARCHER.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": ""})

    def description(self):
        return "Sync the project with the latest changes"
    
    def instructions(self):
        return [ "The command is used to sync the project with the latest changes."]