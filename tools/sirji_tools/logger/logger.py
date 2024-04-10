import os
import logging
import time

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

class UnixTimestampFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        return f"{int(time.time())}"
    
# Singleton class to create loggers
class LoggerSingleton:

    def __init__(self, file_name, log_level):
        self.logger = self._setup_logger(file_name, log_level)
    
    def _log_folder(self):
        return os.path.join(self._get_workspace_folder(), '.sirji', self._get_run_id_folder(), "logs")
    
    def _get_workspace_folder(self):
        workspace = os.environ.get("SIRJI_WORKSPACE")
        if workspace is None:
            raise ValueError(
                "SIRJI_WORKSPACE is not set as an environment variable")
        return workspace

    def _get_run_id_folder(self):
        run_id = os.environ.get("SIRJI_RUN_ID")
        if run_id is None:
            raise ValueError(
                "SIRJI_RUN_ID is not set as an environment variable")
        return run_id 
    
    def _log_file_path(self, file_name):
        return os.path.join(self._log_folder(), file_name)
        
    def _setup_logger(self, file_name, log_level):
        # Create a folder named "logs" if it doesn't exist
        if not os.path.exists(self._log_folder()):
            os.makedirs(self._log_folder())
        
        logger = logging.getLogger(file_name)
        logger.setLevel(log_level)
        if not logger.handlers:
            # Ensure no duplicate handlers
            file_handler = logging.FileHandler(self._log_file_path(file_name))
            formatter = UnixTimestampFormatter('[%(asctime)s] %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        logger.filepath = self._log_file_path(file_name)

        # Attach the initializeLogs method
        def initialize_logs(self, msg):
            original_formatter = self.handlers[0].formatter
            simple_formatter = logging.Formatter('%(message)s')  # Formatter without Unix timestamp
            try:
                # Temporarily change formatter to log without timestamp
                self.handlers[0].setFormatter(simple_formatter)
                self.info(msg)
            finally:
                # Revert to original formatter
                self.handlers[0].setFormatter(original_formatter)
        
        # Monkey patch the logger instance
        logger.initialize_logs = initialize_logs.__get__(logger)
        
        return logger

# Manager class to create and manage loggers
class LoggerManager:
    def __init__(self):
        self._coder = LoggerSingleton('coder.log', _default_log_level).logger
        self._researcher = LoggerSingleton('researcher.log', _default_log_level).logger
        self._planner = LoggerSingleton('planner.log', _default_log_level).logger
        self._executor = LoggerSingleton('executor.log', _default_log_level).logger
        self._sirji = LoggerSingleton('sirji.log', _default_log_level).logger
        self._user = LoggerSingleton('user.log', _default_log_level).logger

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
    
    @property
    def user(self):
        return self._user

logger = LoggerManager()