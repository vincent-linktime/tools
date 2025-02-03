# logging.py
import logging
import sys
import os

def setup_logger(name: str,
                 log_file: str = None,
                 level: int = logging.DEBUG,
                 fmt: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s") -> logging.Logger:
    """
    Set up a logger with the specified name and configuration.

    :param name: The name of the logger (usually __name__ of the calling module).
    :param log_file: If provided, logs will also be written to this file.
    :param level: Logging level (e.g., logging.DEBUG, logging.INFO).
    :param fmt: Logging format.
    :return: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # If logger already has handlers, avoid adding duplicates
    if logger.handlers:
        return logger

    # Formatter for logging messages
    formatter = logging.Formatter(fmt)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler, if a log_file path is provided
    if log_file:
        # Ensure the directory for the log file exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Example: Creating a module-level logger that can be imported elsewhere.
# This logger writes to the console, and optionally you can specify a log file.
default_logger = setup_logger(__name__)
