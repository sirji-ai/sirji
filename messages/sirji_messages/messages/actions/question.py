import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class QuestionMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.QUESTION.name
        self.to_agent = AgentEnum.SIRJI_USER.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "Empty",
            "body": textwrap.dedent("""
            {{Question}}""")})

    def description(self):
        return "Ask a question"
    
    def instructions(self):
        return []