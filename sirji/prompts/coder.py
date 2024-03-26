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

            # //- Generate structured and modular code to solve the problem. Ensure that your code is not commented.
            # //- Never use the example APIs in the code. Research if not in your knowledge.
            # //- Use Python, if the programming language cannot be inferred from PS.
            # //- Import/require already created files. 
            # //- Execute the generated code and analyze the output. If any errors, try to fix them.
            # //- Ensure that the code returns the required response apart from printing it to the console.
            # //- Generate README markdown files explaining the generated code.
            # //- Install required packages, libraries, and dependencies to execute the generated code.

    def responsibilities_prompt(self):
        return textwrap.dedent(f"""
            - Pay close attention to PS and try to programmatically solve it as asked.
            - Follow secure software development practices while generating code.
            - Identify URLs or terms (outside of your knowledge) in the PS, which you want to be trained on or researched. After training, infer from the trained content/knowledge. If the response of the inference has new URLs or terms (outside of your knowledge), you can get trained on them as well.
            - Generate a list of non-technical steps before code generation.
            - Always notify the step, before starting the work on it.
            - Always notify the completed step, before moving to the next step. 
            - Always notify only one step status at a time.
            - Use Python, if the programming language cannot be inferred from PS.
            - Ensure that you write files inside the "workspace/code" folder.
            - Navigate to the workspace folder using 'cd' command, then execute all subsequent commands. Example `cd <<workspace folder>> && <<your executable>>`
            - Always execute the code and evaluate the response output. If response has errors, solve them before before moving ahead.
            - Only interact with the agents listed below using the allowed responses, also mentioned below.
            - Ensure the response is also enclosed inside 3 backticks (```).
            - End the conversation if you find that the PS cannot be solved programmatically or your solution is complete.
            """)

    def capabilities_prompt(self):
        return ""  # This should not be called.

    def interact_with(self):
        return [
            UserPrompt(self.name(), self.short_name()),
            PlannerPrompt(self.name(), self.short_name()),
            ResearcherPrompt(self.name(), self.short_name()),
            ExecutorPrompt(self.name(), self.short_name())
        ]

    def incoming_message_instances(self):
        return []

    def outgoing_message_instances(self):
        return []

    def ending_prompt(self):
        return ""
