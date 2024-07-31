from sirji_messages import AgentEnum, ActionEnum;
from .base import BaseMessages;

class DoNothing(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.DO_NOTHING.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": "{{Provide the reason why the agent is doing nothing.}}"})

    def description(self):
        return "Do Nothing"
    
    def instructions(self):
        return [ "The command is used to do nothing."]
