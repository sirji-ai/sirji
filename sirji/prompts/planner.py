import textwrap

from sirji.messages.elaborated_problem_statement import ElaboratedProblemStatementMessage

from sirji.messages.steps import StepsMessage

from .base import PromptGeneratorBase


class PlannerPrompt(PromptGeneratorBase):

    def __init__(self, caller_name, caller_short_name):
        super().__init__(caller_name, caller_short_name)

    def name(self):
        return "Planning Agent"

    def short_name(self):
        return "Planner"

    def intro_prompt(self):
        return textwrap.dedent(f"""
          You are a {self.name()} ({self.short_name()}), helping generate a list of non-technical steps required to solve the given problem statement (PS).
          """)

    def responsibilities_prompt(self):
        return textwrap.dedent(f"""
          - Pay close attention to PS while generating non-technical steps to solve the problem programmatically.
          - Use Python, if the programming language cannot be inferred from PS.
          - Don't explain the steps further using sub-steps.
          - Generate concise steps enough to solve the problem statement.
          - Ensure that all the steps should be about either create file or install package or execute command or execute code to debug.
          - Always add a step to execute the code and evaluate the response output. If the response has errors, solve them before moving ahead.
          - Add steps to read from external files by using a combination of wget and cat commands.
          - Focus on particular datapoints given in the PS and not solve the problem in a over-generalized manner.
          """)

    def capabilities_prompt(self):
        return textwrap.dedent("""
          - Generate non-technical steps to solve the problem programmatically.
          """)

    def interact_with(self):
        return []

    def incoming_message_instances(self):
        return [ElaboratedProblemStatementMessage(self.short_name())]

    def outgoing_message_instances(self):
        return [StepsMessage(self.short_name())]

    def ending_prompt(self):
        return ""
