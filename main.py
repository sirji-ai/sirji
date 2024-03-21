import argparse
import sys
import uuid
import os
import textwrap

from sirji.view.terminal import open_terminal_and_run_command
from sirji.view.screen import get_screen_resolution
from sirji.tools.logger import coder as cLogger
from sirji.tools.logger import researcher as rLogger
from sirji.tools.logger import planner as pLogger
from sirji.tools.logger import executor as eLogger
from sirji.tools.logger import sirji as sLogger
from sirji.agents.coder import Coder
from sirji.messages.problem_statement import ProblemStatementMessage


class Main():
    def __init__(self):
        self.problem_statement = None  # Placeholder
        self.initialize_logs()

    def read_arguments(self):
        # Create ArgumentParser object
        parser = argparse.ArgumentParser(description="Process some inputs.")

        # Add the 'ps' argument
        parser.add_argument('--ps', type=str, help='Your problem statement')

        # Parse the arguments
        args = parser.parse_args()

        self.problem_statement = args.ps

        if self.problem_statement:
            print(f"Problem statement: {self.problem_statement}")
        else:
            print("No problem statement was provided. Exiting.")
            sys.exit(1)

    def initialize_logs(self):
        # Empty the files
        open(cLogger.filepath, 'w').close()
        open(rLogger.filepath, 'w').close()
        open(pLogger.filepath, 'w').close()
        open(eLogger.filepath, 'w').close()
        open(sLogger.filepath, 'w').close()

        # Initialize the logs
        cLogger.info("Initializing logs")
        rLogger.info("Initializing logs")
        pLogger.info("Initializing logs")
        eLogger.info("Initializing logs")
        sLogger.info("Initializing logs")

    def open_views(self):
        screen_width, screen_height = get_screen_resolution()
        margin = 5  # Margin size in pixels
        window_width = (screen_width - 3 * margin) // 2
        window_height = (screen_height - 22 - 4 * margin) // 3

        command_title_pairs = [
            (f"echo Welcome to Sirji;tail -f {sLogger.filepath}",
             "Sirji Chat"),
            (f"tail -f {sLogger.filepath}", "Sirji Logs"),
            (f"tail -f {pLogger.filepath}", "Planner Logs"),
            (f"tail -f {rLogger.filepath}", "Researcher Logs"),
            (f"tail -f {cLogger.filepath}", "Coder Logs"),
            (f"tail -f {eLogger.filepath}", "Executor Logs")
        ]

        current_directory = os.getcwd()

        # Prepend `cd {current_directory} &&` to each command to ensure it runs in the desired directory
        command_title_pairs = [(f"cd {current_directory} && {command}", title)
                               for command, title in command_title_pairs]

        for i, (command, title) in enumerate(command_title_pairs):
            open_terminal_and_run_command(
                command, title, i, window_width, window_height)

    def pass_user_input_to_coder():
        pass

    def start(self):
        self.read_arguments()
        self.open_views()


if __name__ == "__main__":
    Main().start()
