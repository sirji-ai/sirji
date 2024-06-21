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
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": "{{notes}}"})

    def description(self):
        return "Store Notes in the scratchpad"
    
    def instructions(self):
        return [ "The command is used to store notes in the scratchpad.",]
