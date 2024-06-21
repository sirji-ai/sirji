import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class ExecuteCommandMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.EXECUTE_COMMAND.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            {{command}}""")})

    def description(self):
        return "Execute a Command, Install Packages, or Install Dependencies"
    
    def instructions(self):
        return [ "The command must use the project root as the current working directory.",
                 "The command must be sufficiently chained. For example, 'source venv/bin/activate && pip install openai', 'cd server && npm run start'."]
