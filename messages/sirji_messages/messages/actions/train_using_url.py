import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class TrainUsingUrlMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.TRAIN_USING_URL.name
        self.to_agent = AgentEnum.RESEARCHER.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "summary": "{{A concise summary to be displayed to the user for the action to be performed.}}",
            "body": textwrap.dedent("""
            URL: {{url}}
            """)})

    def description(self):
        return "Train using a URL:"
