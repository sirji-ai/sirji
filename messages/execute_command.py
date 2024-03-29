import textwrap

from base import BaseMessages

class ExecuteCommandMessage(BaseMessages):

    def template(self):
        return textwrap.dedent("""
        ```
        FROM: {interactor}
        TO: {implementor}
        ACTION: execute-command
        COMMAND: {command}							 
        ```
        """)

    def sample(self, interactor):
        return self.generate(interactor, {
            "command": "Command to execute."
        })

    def description(self):
        return "To execute a command:"

    @staticmethod
    def properties():
        return ['FROM', 'TO', 'ACTION', 'COMMAND']
