import os
import subprocess
from sirji.messages.output import OutputMessage
from sirji.tools.logger import executor as logger
from sirji.messages.parser import MessageParser


class SingletonMeta(type):
    """
    This is a metaclass that will be used to create a Singleton class.
    It ensures that only one instance of the Singleton class exists.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


workspace_dir = os.path.join(os.getcwd(), 'workspace', 'code')


class Executor(metaclass=SingletonMeta):
    def _workspace_dir(self):
        if not os.path.exists(workspace_dir):
            logger.info("Creating workspace dir.")
            os.makedirs(workspace_dir, exist_ok=True)

        return workspace_dir

    def create_file(self, parsedMessage):
        file_path = os.path.join(
            self._workspace_dir(), parsedMessage.get("FILENAME").strip())
        content = parsedMessage.get("CONTENT")
        directory_path = os.path.dirname(file_path)

        if not os.path.exists(directory_path):
            logger.info("Creating directories for the new file.")
            os.makedirs(directory_path, exist_ok=True)

        logger.info(f"Creating file at path: {file_path}")
        try:
            with open(file_path, "w") as file:
                file.write(content)
                logger.info(f"File created successfully: {file_path}")
                return "Done"
        except Exception as e:
            logger.error(
                f"Failed to create or write to the file '{file_path}'. Error: {e}")
            return f"Failed to create or write to the file '{file_path}'. Error: {e}"

    def execute_command(self, command):
        try:
            logger.info(
                f"Executing command in {self._workspace_dir()}: {command}")
            result = subprocess.run(command, shell=True, cwd=self._workspace_dir(), check=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=180)

            logger.info(f"Command executed successfully: {command}")
            return result.stdout

        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing command '{command}': {e.stderr}")
            return e.stderr
        except subprocess.TimeoutExpired as e:
            logger.error(f"Command '{command}' timed out")
            return 'Execution timeout'

    def message(self, input_message):
        parsedMessage = MessageParser.parse(input_message)
        action = parsedMessage.get("ACTION")
        messageFrom = parsedMessage.get("FROM")
        messageTo = parsedMessage.get("TO")

        logger.info(
            f"Received message from: {messageFrom} with action: {action}")

        if action == "create-file":
            details = self.create_file(parsedMessage)
        elif action == "execute-command":
            details = self.execute_command(
                parsedMessage.get("COMMAND").strip())
        elif action == "install-package":
            details = self.execute_command(
                parsedMessage.get("COMMAND").strip())
        else:
            logger.error(f"Unknown action: {action}")
            raise ValueError(f"Unknown action: {action}")

        logger.info("Preparing output message")
        output_instance = OutputMessage(messageTo)
        output_message = output_instance.generate(
            messageFrom, {"details": details})

        return output_message
