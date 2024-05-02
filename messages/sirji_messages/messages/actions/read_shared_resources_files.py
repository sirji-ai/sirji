import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class ReadSharedResourcesFilesMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.READ_SHARED_RESOURCES_FILES.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            File paths: {{Array of file paths}}""")})
    
    def description(self):
        return "Read Multiple Files From Shared Resources"
    
    def instructions(self):
        return [ "The file paths must be in the following format: '{{Your Agent ID}}/{{file name}}'."]
