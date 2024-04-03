import textwrap
from abc import ABC, abstractmethod


class BaseMessages(ABC):

    @abstractmethod
    def template_payload_part(self):
        """
        Message template's payload part which is custom to the message action.
        """
        pass

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

    @staticmethod
    @abstractmethod
    def custom_properties():
        """
        List of custom properties of the message.
        """
        pass

    def generate(self, obj):
        return self.template().format(**obj)

    def template_prefix_part(self):
        return textwrap.dedent(f"""
            ```
            FROM: {self.from_agent}
            TO: {self.to_agent}
            ACTION: {self.action}""")

    def template_suffix_part(self):
        return textwrap.dedent(f"""```
            """)

    def template(self):
        return self.template_prefix_part() + self.template_payload_part() + self.template_suffix_part()
