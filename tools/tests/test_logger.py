import pytest
from unittest.mock import patch, MagicMock
from sirji_tools.logger import LoggerManager

class TestLoggerManager:
    @patch('sirji_tools.logger.logger.logging')
    def test_logger_manager_initialization(self, mock_logging):
        # Setup
        mock_logging.getLogger.return_value = MagicMock()

        # Test LoggerManager initialization
        logger_manager = LoggerManager()

        # Assertions to ensure that logger instances are created
        assert logger_manager.coder is not None, "LoggerManager did not initialize a coder logger."
        assert logger_manager.researcher is not None, "LoggerManager did not initialize a researcher logger."
        assert logger_manager.planner is not None, "LoggerManager did not initialize a planner logger."
        assert logger_manager.executor is not None, "LoggerManager did not initialize an executor logger."
        assert logger_manager.sirji is not None, "LoggerManager did not initialize a sirji logger."
        assert logger_manager.user is not None, "LoggerManager did not initialize a user logger."

    @patch('sirji_tools.logger.logger.logging')
    def test_logger_manager_logging(self, mock_logging):
        # Setup
        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger

        # Test logging through LoggerManager
        logger_manager = LoggerManager()
        logger_manager.coder.info("Test message for coder")
        logger_manager.researcher.info("Test message for researcher")
        logger_manager.planner.info("Test message for planner")
        logger_manager.executor.info("Test message for executor")
        logger_manager.sirji.info("Test message for sirji")
        logger_manager.user.info("Test message for user")

        # Verify
        mock_logger.info.assert_any_call("Test message for coder"), "LoggerManager's coder did not log message correctly."
        mock_logger.info.assert_any_call("Test message for researcher"), "LoggerManager's researcher did not log message correctly."
        mock_logger.info.assert_any_call("Test message for planner"), "LoggerManager's planner did not log message correctly."
        mock_logger.info.assert_any_call("Test message for executor"), "LoggerManager's executor did not log message correctly."
        mock_logger.info.assert_any_call("Test message for sirji"), "LoggerManager's sirji did not log message correctly."
        mock_logger.info.assert_any_call("Test message for user"), "LoggerManager's user did not log message correctly."