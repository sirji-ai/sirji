import textwrap
from abc import ABC, abstractmethod

class BaseMessages(ABC):

    @abstractmethod
    def sample(self):
        """
        Sample message using the message template.
        """
        pass

    @abstractmethod
    def description(self):
        """
        Description of the message.
        """
        pass

    @abstractmethod
    def instructions(self):
        """
        Instructions for the message.
        """
        pass

    def generate(self, obj):

        try:
            if self.to_agent:
                obj["to_agent_id"] = self.to_agent
        except AttributeError:
            pass

        try:
            if self.from_agent:
                obj["from_agent_id"] = self.from_agent
        except AttributeError:
            pass
            
        return self.template().format(**obj)
    
    def template(self):
        return textwrap.dedent(f"""
            ***
            FROM: {{from_agent_id}}
            TO: {{to_agent_id}}
            ACTION: {self.action}
            STEP: "Provide the step number here for the ongoing step if any."
            SUMMARY: {{summary}}
            BODY: {{body}}
            ***""")
