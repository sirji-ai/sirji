import argparse
import sys
import uuid
import os
import shutil
import textwrap
import re

from sirji.view.terminal import open_terminal_and_run_command
from sirji.view.screen import get_screen_resolution

from sirji.tools.logger import coder as cLogger
from sirji.tools.logger import researcher as rLogger
from sirji.tools.logger import planner as pLogger
from sirji.tools.logger import executor as eLogger
from sirji.tools.logger import sirji as sLogger
from sirji.tools.logger import user as uLogger

from sirji.agents.coder import Coder
from sirji.agents.planner import Planner
from sirji.agents.researcher import Researcher
from sirji.agents.executor import Executor
from sirji.agents.user import User

from sirji.messages.parser import MessageParser


from sirji.messages.problem_statement import ProblemStatementMessage

last_recipient = ''


class Main():
    def __init__(self):
        self.problem_statement = None  # Placeholder
        self.empty_workspace()
        self.initialize_logs()

        self.coder = Coder()
        self.planner = Planner()
        self.researcher = Researcher('openai_assistant', 'openai_assistant')
        self.executor = Executor()
        self.user = User()

    def read_arguments(self):
        # Create ArgumentParser object
        parser = argparse.ArgumentParser(description="Process some inputs.")

        # Add the 'ps' argument
        parser.add_argument('--ps', type=str, help='Your problem statement')

        # Parse the arguments
        args = parser.parse_args()

        self.problem_statement = args.ps

        if self.problem_statement:
            sLogger.info(
                f"Going to Coder with the problem statement: {self.problem_statement}")
            print(f"Problem statement: {self.problem_statement}")
        else:
            print("No problem statement was provided. Exiting.")
            sys.exit(1)

    def empty_workspace(self):
        workspace_dir = "workspace"

        # List all files and directories in the workspace directory
        for item in os.listdir(workspace_dir):
            if (item == "logs"):
                continue  # Skip the code directory

            item_path = os.path.join(workspace_dir, item)

            try:
                # If it's a directory, remove it along with its contents
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                # If it's a file, remove it
                else:
                    os.remove(item_path)
            except Exception as e:
                print(f"Error removing {item_path}: {e}")

    def truncate_logs(self):
        # List of loggers
        loggers = [cLogger, rLogger, pLogger, eLogger, sLogger, uLogger]

        for logger in loggers:
            # Check if logger is present
            if logger is not None:
                try:
                    # Check if the file exists at the given location
                    if os.path.exists(logger.filepath):
                        # File exists, so open it in 'w' mode to clear or create it, then immediately close it
                        open(logger.filepath, 'w').close()
                    else:
                        # If the file does not exist, handle accordingly (e.g., log this situation or take other actions)
                        print(f"File does not exist at {logger.filepath}.")

                except AttributeError:
                    # Handle the case where the logger doesn't have a 'filepath' attribute
                    print(
                        f"Logger {logger} does not have a 'filepath' attribute.")

                except IOError as e:
                    # Handle other I/O errors, such as permission errors
                    print(
                        f"Failed to open file for logger {logger} at {logger.filepath}: {e}")

    def initialize_logs(self):
        # Truncate the logs
        self.truncate_logs()

        # Initialize the logs
        cLogger.initialize_logs(
            "Coder: Specializing in generating and modifying code, this agent is skilled in various programming languages and is equipped to handle tasks ranging from quick fixes to developing complex algorithms.\n\n\n")

        rLogger.initialize_logs("Researcher: dives into vast pools of information to find answers, evidence, or data that support the task at hand. Whether it's through browsing the web, accessing databases, or consulting academic journals, this agent is adept at gathering and synthesizing relevant information to aid in problem-solving.\n\n\n")

        pLogger.initialize_logs("Planner: planner is tasked with orchestrating the overall strategy for solving user queries. Assesses the problem statement and determines the most effective sequence of actions, delegating tasks to other agents and tools as necessary. This agent ensures that Sirji's workflow is efficient and goal-oriented.\n\n\n")

        eLogger.initialize_logs("Executor: responsible for running code or scripts in a controlled environment, allowing for executing and testing activities. Executor verifies the correctness and efficacy of solutions before they are finalized and implements automated tasks as defined by the Planner.\n\n\n")

        sLogger.initialize_logs(
            "Sirji: Sirji will automatically create a plan to solve the problem statement, prioritize it, organize research, write code, execute it, and fix issues.\n\n\n")

        uLogger.initialize_logs(
            "User: The user is the person who interacts with Sirji. The user can ask questions, provide problem statements, and receive solutions from Sirji.\n\n\n")

    def open_views(self):
        screen_width, screen_height = get_screen_resolution()
        margin = 5  # Margin size in pixels
        window_width = (screen_width - 3 * margin) // 2
        window_height = (screen_height - 22 - 4 * margin) // 3

        command_title_pairs = [
            (f"tail -f {sLogger.filepath}", "Sirji"),
            (f"watch -n 1 'cat {pLogger.filepath}'", "Plan Progress"),
            (f"tail -f {rLogger.filepath}", "Research Agent"),
            (f"tail -f {cLogger.filepath}", "Coding Agent"),
            (f"tail -f {eLogger.filepath}", "Execution Agent")
        ]

        current_directory = os.getcwd()

        # Prepend `cd {current_directory} &&` to each command to ensure it runs in the desired directory
        command_title_pairs = [(f"cd {current_directory} && {command}", title)
                               for command, title in command_title_pairs]

        for i, (command, title) in enumerate(command_title_pairs):
            open_terminal_and_run_command(
                command, title, i, window_width, window_height)

    def _parse_response(self, response_str):
        """
        Parses the response string to a dictionary.
        """
        print(response_str)
        response = MessageParser.parse(response_str)
        return response

    def handle_response(self, message):
        """
        Recursively passes the response object among different objects.
        """

        global last_recipient  # Declare that we intend to use the global variable

        try:
            response = self._parse_response(message)
            recipient = response.get("TO").strip()
            sender = response.get("FROM").strip()
            action = response.get("ACTION").strip()
        except Exception as e:
            recipient = last_recipient
            message = textwrap.dedent(f"""
              ```
              FROM: User
              TO: {recipient}
              ACTION: acknowledge
              DETAILS: Sure.
              ```
              """)
            response = self._parse_response(message)
            recipient = response.get("TO").strip()
            sender = response.get("FROM").strip()
            action = response.get("ACTION").strip()

        sLogger.info(
            f"Forwarding message from {sender} to {recipient} for action: {action}")

        if (action == "solution-complete"):
            details = response.get("DETAILS")
            sLogger.info(f"Solution complete: {details}")

        response_message = ''

        # Pass the response to the appropriate object and update the response object.
        if recipient == "Coder":
            response_message = self.coder.message(message)
        elif recipient == "Planner":
            response_message = self.planner.message(message)
        elif recipient == "Executor":
            response_message = self.executor.message(message)
        elif recipient == "Researcher":
            response_message = self.researcher.message(message)
        elif recipient == "User":
            response_message = self.user.message(message)
            # Optionally, insert a return or break statement if 'UR' is a terminal condition.
        else:
            raise ValueError(f"Unknown recipient type: {recipient}")

        last_recipient = recipient

        self.handle_response(response_message)

    def start(self):
        self.read_arguments()
        self.open_views()

        ps_message = self.user.generate_problem_statement_message(
            self.problem_statement, 'Coder')

        response_message = self.coder.message(ps_message)

        self.handle_response(response_message)


if __name__ == "__main__":
    Main().start()
