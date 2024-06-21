import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages


class ReadAgentOutputFilesMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.READ_AGENT_OUTPUT_FILES.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            File paths: {{Array of file paths}}""")})
    
    def description(self):
        return "Read Multiple Files From Agent Output Folder"
    
    def instructions(self):
        return [ "The body must be in the following format: File paths: [\{{Your_agent_id}}/{{file_name}}\]"]
    
