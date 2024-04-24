import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class AppendToSharedResourceIndexMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.APPEND_TO_SHARED_RESOURCES_INDEX.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "summary": "{{A concise summary to be displayed to the user for the action to be performed.}}",
            "body": textwrap.dedent("""
            File path: {{file path of the shared resource file relative to the shared_resource folder}}
            ---
            {{Description of the shared resource file, to be used by other agents to know what it is about}}
            """)})

    def description(self):
        return "To append to shared resource index:"
