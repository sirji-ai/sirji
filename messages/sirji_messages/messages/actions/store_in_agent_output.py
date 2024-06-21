import textwrap

from sirji_messages import AgentEnum, ActionEnum
from .base import BaseMessages

class StoreInAgentOutputMessage(BaseMessages):

    def __init__(self):
        self.action = ActionEnum.STORE_IN_AGENT_OUTPUT.name
        self.to_agent = AgentEnum.EXECUTOR.name

        super().__init__()

    def sample(self):
        return self.generate({
            "from_agent_id": "{{Your Agent ID}}",
            "step": "Provide the step number here for the ongoing step if any.",
            "summary": "{{{Display a concise summary to the user, describing the action using the present continuous tense.}}",
            "body": textwrap.dedent("""
            File path: {{file path}}
            ---
            File content: {{file contents}}                     
            ---
            File content description: {{Description of the agent output file, to be used by other agents to know what it is about}}""")})

    def description(self):
        return "Create a file in the Agent Output Folder and register it to the Agent Output Index file"
    
    def instructions(self):
        return [ "The file path must be in the following format: '{{Your Agent ID}}/{{file name}}'."]

