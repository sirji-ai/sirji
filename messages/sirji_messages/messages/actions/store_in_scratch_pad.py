import textwrap;

from sirji_messages import AgentEnum, ActionEnum;
from .base import BaseMessages;

class StoreInScratchPad(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.STORE_IN_SCRATCH_PAD.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": "{{notes}}"})

    def description(self):
        return "Save Notes in the Scratch Pad"
    
    def instructions(self):
        return [ "The command is used to save the notes in the scratch pad.",]