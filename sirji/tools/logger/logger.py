import os
import logging

# Mapping of log level strings to constants
_log_level_str_to_const = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

# Set default log level to DEBUG
_default_log_level = _log_level_str_to_const.get(os.environ.get("SIRJI_LOG_LEVEL", 'debug').lower())

# Singleton class to create loggers
class LoggerSingleton:
    def __init__(self, file_name, log_level):
        self.logger = self._setup_logger(file_name, log_level)

    def _setup_logger(self, file_name, log_level):
        # Create a folder named "logs" if it doesn't exist
        log_folder = os.path.join("workspace", "logs")
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        # Set up logging
        log_file_path = os.path.join(log_folder, file_name)
        logger = logging.getLogger(file_name)
        logger.setLevel(log_level)
        if not logger.handlers:
            # Ensure no duplicate handlers
            file_handler = logging.FileHandler(log_file_path)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        return logger

# Manager class to create and manage loggers
class LoggerManager:
    def __init__(self):
        self._coder = LoggerSingleton('coder.log', _default_log_level).logger
        self._researcher = LoggerSingleton('researcher.log', _default_log_level).logger
        self._planner = LoggerSingleton('planner.log', _default_log_level).logger
        self._executor = LoggerSingleton('executor.log', _default_log_level).logger
        self._sirji = LoggerSingleton('sirji.log', _default_log_level).logger

    @property
    def coder(self):
        return self._coder

    @property
    def researcher(self):
        return self._researcher
    
    @property
    def planner(self):
        return self._planner
    
    @property
    def executor(self):
        return self._executor
    
    @property
    def sirji(self):
        return self._sirji

logger = LoggerManager()