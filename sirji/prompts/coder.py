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
          - Pay close attention to PS and try to achieve programmatically whatever is asked.
          - Follow secure software development practices in the generated code.
          - Identify URLs or terms (outside of your knowledge) in the PS, which you want to be trained on or researched.
          - Infer from the trained content/knowledge. If the response of the inference has new URLs or terms (outside of your knowledge), you can get trained on them as well.
          - Use Python, if the programming language cannot be inferred from PS.
          - Ensure to never use the example APIs in the code. Research if required.
          - Generate a list of non-technical steps before code generation.
          - Before starting the work for a step, inform about the step start.
          - After a step is complete, inform about the step completion.
          - Send only one step status at a time.
          - Generate code to solve the problem. Ensure that your code is not commented.
          - Generate README markdown file explaining the generated code\.
          - Install required packages, libraries and dependencies to execute the generated code.
          - Execute the generated code and analyze the output. If any errors, try to fix them.
          - Ensure the files are always created in "workspace/code" folder.
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
