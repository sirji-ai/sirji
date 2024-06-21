import textwrap;

from sirji_messages import AgentEnum, ActionEnum;

from .base import BaseMessages;

class LogSteps(BaseMessages):
    def __init__(self):
        self.action = ActionEnum.LOG_STEPS.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            Steps: {{Array of steps}}""")})
    
    def description(self):
        return "Log Steps"
    
    def instructions(self):
        return [ "The body must be in the following format: Steps: [{step_1 :step_description }, {step_2 : step_description}]",
                "Make sure the steps inside the array is valid JSON format both key-value pairs should be in double quotes."
            ]