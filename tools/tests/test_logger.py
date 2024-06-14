import pytest
from unittest.mock import patch, MagicMock
from sirji_tools.logger import logger_manager


class TestLoggerManager:
    @patch('sirji_tools.logger.logger.logging.getLogger')
    def test_logger_manager_initialization(self, mock_get_logger):
        # Setup
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Test logger_manager initialization
        assert logger_manager.orchestrator is not None, "LoggerManager did not initialize an orchestrator logger."


    @patch('sirji_tools.logger.logger.logging.getLogger')
    def test_logger_manager_logging(self, mock_get_logger):
        # Setup
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Test logging through logger_manager
        logger_manager.orchestrator.info("Test message for orchestrator")


    @patch('sirji_tools.logger.logger.logging.getLogger')
    def test_create_logger(self, mock_get_logger):
        # Setup
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Test create_logger method
        new_logger = logger_manager.create_logger("new_logger.log", "info")
        new_logger.info("Test message for new logger")

        # Verify
        mock_logger.info.assert_any_call("Test message for new logger")