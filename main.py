import argparse
import sys
import uuid
import os
import textwrap
import re

from sirji.view.terminal import open_terminal_and_run_command
from sirji.view.screen import get_screen_resolution

from sirji.tools.logger import coder as cLogger
from sirji.tools.logger import researcher as rLogger
from sirji.tools.logger import planner as pLogger
from sirji.tools.logger import executor as eLogger
from sirji.tools.logger import sirji as sLogger

from sirji.agents.coder import Coder
from sirji.agents.planner import Planner
from sirji.agents.researcher import Researcher
from sirji.agents.executor import Executor


from sirji.messages.problem_statement import ProblemStatementMessage


class Main():
    def __init__(self):
        self.problem_statement = None  # Placeholder
        self.initialize_logs()
        self.coder = Coder()
        self.planner = Planner()
        self.researcher = Researcher('openai_assistant', 'openai_assistant')
        self.executor = Executor()

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
        cLogger.info("****** Coder: Specializing in generating and modifying code, this agent is skilled in various programming languages and is equipped to handle tasks ranging from quick fixes to developing complex algorithms.\n\n\n")

        rLogger.info("****** Researcher: dives into vast pools of information to find answers, evidence, or data that support the task at hand. Whether it's through browsing the web, accessing databases, or consulting academic journals, this agent is adept at gathering and synthesizing relevant information to aid in problem-solving.\n\n\n")

        pLogger.info("****** Planner: planner is tasked with orchestrating the overall strategy for solving user queries. Assesses the problem statement and determines the most effective sequence of actions, delegating tasks to other agents and tools as necessary. This agent ensures that Sirji's workflow is efficient and goal-oriented.\n\n\n")

        eLogger.info("****** Executor: responsible for running code or scripts in a controlled environment, allowing for executing and testing activities. Executor verifies the correctness and efficacy of solutions before they are finalized and implements automated tasks as defined by the Planner.\n\n\n")

        sLogger.info("****** Sirji: Sirji will automatically create a plan to solve the problem statement, prioritize it, organize research, write code, execute it, and fix issues.\n\n\n")

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

    def _parse_response(self, response_str):
        """
        Parses the response string to a dictionary.
        """
        response = {}
        for line in response_str.split('\n'):
            if line:
                key, val = line.split(': ')
                response[key.strip()] = val.strip()
        return response

    def handle_response(self, response_str):
        """
        Recursively passes the response object among different objects.
        """
        response = self._parse_response(response_str)

        # Extract the 'TO' field from the response object.
        recipient = response.get("TO")

        # Pass the response to the appropriate object and update the response object.
        if recipient == "CR":
            response_str = self.coder.message(response)
        elif recipient == "PA":
            response_str = self.planner.message(response)
        elif recipient == "ER":
            response_str = self.executor.message(response)
        elif recipient == "RA":
            response_str = self.researcher.message(response)
        elif recipient == "UR":
            response_str = self.user.message(response)
            # Optionally, insert a return or break statement if 'UR' is a terminal condition.
        else:
            raise ValueError(f"Unknown recipient type: {recipient}")

        self.handle_response(response_str)

    def start(self):
        self.read_arguments()
        # self.open_views()

        response_str = self.coder.message(self.problem_statement)

        print(response_str)

        self.handle_response(response_str)

        # parse response to get 'to' field

        # if to is CR, call `response = self.coder.message(response)`
        # if to is PA, call `response = self.planner.message(response)`
        # if to is ER, call `response = self.executor.message(response)`
        # if to is RA, call `response = self.researcher.message(response)`
        # if to is UR, call `response = self.user.message(response)`


if __name__ == "__main__":
    Main().start()
