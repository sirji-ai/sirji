import os
import logging

class LoggerSingleton:
    _instances = {}

    def __new__(cls, file_name, log_level=logging.INFO):
        if file_name not in cls._instances:
            cls._instances[file_name] = super().__new__(cls)
            cls._instances[file_name]._setup_logger(file_name, log_level)
        return cls._instances[file_name]

    def _setup_logger(self, file_name, log_level):
        # Create a folder named "log" if it doesn't exist
        log_folder = os.path.join("workspace", "logs")
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        # Set up logging
        log_file_path = os.path.join(log_folder, file_name)
        logging.basicConfig(filename=log_file_path, level=log_level,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()

def get_logger(file_name, log_level=logging.INFO):
    return LoggerSingleton(file_name, log_level).logger