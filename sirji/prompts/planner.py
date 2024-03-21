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
          - Don't explain the steps further using sub-steps.
          - Respond with a list of steps.
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
