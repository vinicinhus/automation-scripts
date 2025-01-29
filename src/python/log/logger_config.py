"""
Module: logger_config.py

This module provides a class to configure and manage application logging using Loguru.
The LoggerConfig class sets up different log handlers to capture logs for various levels
such as INFO, ERROR, and DEBUG. It supports logging to the console and multiple log files,
with custom log filenames depending on the environment (development or production). The
module also ensures log rotation and retention to prevent excessive disk usage.

Dependencies:
    - sys: For handling system-related operations like standard output redirection.
    - os: For file path and directory management.
    - loguru: For logging messages with custom formats and advanced configurations.
    - typing.Literal: To enforce environment-specific configurations (development/production).

Usage Example:
    from logger_config import LoggerConfig
    from loguru import logger

    log_config = LoggerConfig(env="development", general_log_file="logs/app.log", error_log_file="logs/error.log")
    logger.info("This is an info message.")
    logger.error("This is an error message.")
    
    # Simulating uncaught exception logging
    raise Exception("This will be logged as an uncaught exception.")
"""

import os
import sys
from typing import TYPE_CHECKING, Literal

from loguru import logger

if TYPE_CHECKING:
    from loguru import Logger


class LoggerConfig:
    """
    A class to configure and manage application logging using Loguru.

    Features:
    - Supports logging to console and files.
    - Allows custom log filenames for different environments.
    - Log rotation and retention policies to prevent excessive disk usage.
    - Automatic capture of uncaught exceptions to log unexpected crashes.
    """

    def __init__(
        self,
        env: Literal["development", "production"] = "development",
        general_log_file: str = "logs/general.log",
        error_log_file: str = "logs/errors.log",
    ) -> None:
        """
        Initializes the logger configuration based on the provided environment.

        Args:
            env (Literal["development", "production"]):
                Defines the environment in which the application is running.
                - "development": Enables console logging for debugging.
                - "production": Disables console logging, logs only to files.

            general_log_file (str):
                Filename for general logs (INFO level and above).

            error_log_file (str):
                Filename for error logs (WARN, ERROR, CRITICAL levels).
        """
        self.env = env
        self.general_log_file = general_log_file
        self.error_log_file = error_log_file

        self._create_log_directories()
        self.configure_logger()

    def _create_log_directories(self) -> None:
        """Creates necessary directories for log files if they do not exist."""
        for log_file in [self.general_log_file, self.error_log_file]:
            log_dir = os.path.dirname(log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)

    def configure_logger(self) -> None:
        """Configures the Loguru logger with multiple handlers for different log levels."""
        # Remove default Loguru handlers to prevent duplicate logs
        logger.remove()

        # 1️ Console Logging (Only for development)
        if self.env == "development":
            logger.add(
                sys.stdout,
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
                level="DEBUG",
            )

        # 2️ General Log File (INFO and above)
        logger.add(
            self.general_log_file,
            rotation="1 day",
            retention="7 days",
            compression="zip",
            level="INFO",
            format="{time} | {level} | {message}",
        )

        # 3️ Error Log File (Only WARN, ERROR, CRITICAL)
        logger.add(
            self.error_log_file,
            rotation="1 week",
            retention="30 days",
            level="ERROR",
            format="{time} | {level} | {message} | {exception}",
        )

    @staticmethod
    def get_logger() -> "Logger":
        """
        Returns the configured Loguru logger instance.

        Returns:
            logger (loguru.logger): The Loguru logger instance ready for use.
        """
        return logger
