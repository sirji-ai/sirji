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
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            Steps: {{Array of steps}}""")})
    
    def description(self):
        return "Log Steps"
    
    def instructions(self):
        return [ "The body must be in the following format: Steps: [\{{step_1 :step_description }}\, \{{step_2 : step_description \]"]