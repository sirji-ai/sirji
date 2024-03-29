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

    # def responsibilities_prompt(self):
    #     return textwrap.dedent(f"""
    #         - Pay close attention to PS and try to programmatically solve it as asked.
    #         - Use Python, if the programming language cannot be inferred from PS.
    #         - Identify URLs or terms (outside of your knowledge) in the PS, which you want to be trained on or researched. After training, infer from the trained content/knowledge. If the response of the inference has new URLs or terms (outside of your knowledge), you can get trained on them as well.
    #         - Get the list of non-technical steps generated before you start solving the problem statement (PS).
    #         - Follow the generated non-technical steps sequentially to solve the PS.
    #         - Ask questions, if essential.                             
    #         - Always notify about the step started before you start working on it. Similarly, notify about the step completed before you move to the next step.
    #         - Follow secure software development practices while generating code.
    #         - Ensure that you don't create any file/folder outside of "workspace/code" folder.
    #         - Navigate to the workspace folder using 'cd' command, then execute all subsequent commands. Example `cd <<workspace folder>> && <<your executable>>`
    #         - Understand the information included in the external files by using a combination of wget and cat commands.
    #         - Only interact with the agents listed below using the allowed responses, also mentioned below.
    #         - Ensure the response is also enclosed inside 3 backticks (```).
    #         - End the conversation if you find that the PS cannot be solved programmatically or your solution is complete.
    #         """)

    def responsibilities_prompt(self):
        return textwrap.dedent(f"""
            - Pay close attention to PS and try to programmatically solve it as asked.
            - Use Python, if the programming language cannot be inferred from PS.
            - Identify URLs (Excluding GitHub) present in the PS, on which you have no knowledge and want to be trained on or researched. After training, infer from the trained content/knowledge. If the response of the inference has new URLs (Excluding GitHub), on which you have no knowledge, you can get trained on them too.
            - Get the list of non-technical steps generated before you start solving the problem statement (PS).
            - Follow the generated non-technical steps sequentially to solve the PS.
            - Ask questions, if essential.                             
            - Always notify about the step started before you start working on it. Similarly, notify about the step completed before you move to the next step.
            - Follow secure software development practices while generating code.
            - Ensure that you don't create any file/folder outside of current directory, i.e. './'
            - Read the GitHub files by first cloning the repository and then reading the files. 
            - Ensure that every code and command execution output is always written in a log file using packages like "tee" and execute in background using "nohup". For example: nohup command | tee <<log file name which can be used to check the output>> &                           
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
            ExecutorPrompt(self.name(), self.short_name()),
            ResearcherPrompt(self.name(), self.short_name())
        ]

    def incoming_message_instances(self):
        return []

    def outgoing_message_instances(self):
        return []

    def ending_prompt(self):
        return ""
