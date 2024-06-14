import os
import logging
import time

_log_level_str_to_const = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

_default_log_level = _log_level_str_to_const.get(os.environ.get("SIRJI_LOG_LEVEL", 'debug').lower())

class UnixTimestampFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        return f"{int(time.time())}"

class LoggerSingleton:
    def __init__(self, file_name, log_level):
        self.logger = self._setup_logger(file_name, log_level)
    
    def _log_folder(self):
        return os.path.join(self._get_run_path(), "logs")
    
    def _get_run_path(self):
        run_id = os.environ.get("SIRJI_RUN_PATH")
        if run_id is None:
            raise ValueError("SIRJI_RUN_PATH is not set as an environment variable")
        return run_id 
    
    def _log_file_path(self, file_name):
        return os.path.join(self._log_folder(), file_name)
        
    def _setup_logger(self, file_name, log_level):
        if not os.path.exists(self._log_folder()):
            os.makedirs(self._log_folder())
        
        logger = logging.getLogger(file_name)
        logger.setLevel(log_level)
        if not logger.handlers:
            file_handler = logging.FileHandler(self._log_file_path(file_name))
            formatter = UnixTimestampFormatter('[%(asctime)s] %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        logger.filepath = self._log_file_path(file_name)

        def initialize_logs(self, msg):
            original_formatter = self.handlers[0].formatter
            simple_formatter = logging.Formatter('%(message)s')
            try:
                self.handlers[0].setFormatter(simple_formatter)
                self.info(msg)
            finally:
                self.handlers[0].setFormatter(original_formatter)
        
        logger.initialize_logs = initialize_logs.__get__(logger)
        
        return logger

class LoggerManager:
    def __init__(self):
        self._orchestrator = LoggerSingleton("orchestrator.log", _default_log_level).logger

    def create_logger(self, file_name, log_level='debug'):
        return LoggerSingleton(file_name, _log_level_str_to_const.get(log_level.lower(), logging.DEBUG)).logger


    @property
    def orchestrator(self):
        return self._orchestrator

logger_manager = LoggerManager()