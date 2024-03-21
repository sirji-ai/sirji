import textwrap

from .planner import PlannerPrompt
from .researcher import ResearcherPrompt
from .executor import ExecutorPrompt
from .user import UserPrompt

from .base import PromptGeneratorBase


class CoderPrompt(PromptGeneratorBase):

    def __init__(self):
        super().__init__(None, None)

    def name(self):
        return "Coding Agent"

    def short_name(self):
        return "Coder"

    def intro_prompt(self):
        return textwrap.dedent(f"""
      You are a {self.name()} ({self.short_name()}), helping programmatically solve a given problem statement (PS).
      """)

    def responsibilities_prompt(self):
        return textwrap.dedent(f"""
      Your job is to:
      - Pay close attention to PS and try to achieve programmatically whatever is asked.
      - Follow secure software development practices in the generated code.
      - Identify URLs or terms (outside of your knowledge) in the PS, which need to be researched. Ask questions on the researched data.
      - Use Python, if the programming language cannot be inferred from PS.
      - Ensure to never use the example APIs in the code. Research if required.
      - Generate a list of non-technical steps before code generation. Keep updating the progress in terms of step start and end.
      - Write code, install required dependencies, and execute required code.
      - Import/require already created files. Try to be as modular as possible.
      - Ensure your code returns the required response apart from printing it to the console.
      - Ensure you end the conversation if you find that the PS cannot be solved programmatically or your solution is complete.

      """)

    def capabilities_prompt(self):
        return ""  # This should not be called.

    def interact_with(self):
        return [
            PlannerPrompt(self.name(), self.short_name()),
            ResearcherPrompt(self.name(), self.short_name()),
            ExecutorPrompt(self.name(), self.short_name()),
            UserPrompt(self.name(), self.short_name())
        ]

    def incoming_message_instances(self):
        return []

    def outgoing_message_instances(self):
        return []

    def ending_prompt(self):
        return ""
