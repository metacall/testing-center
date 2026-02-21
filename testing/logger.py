import logging
import logging.handlers
import os
from datetime import datetime


class Logger:
    """Singleton class to manage the logging"""

    _instance = None

    def __init__(self, log_file=None, max_bytes=10*1024*1024, backup_count=5):
        if Logger._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Logger._instance = self
            self.logger = logging.getLogger("CLI_Tool")
            self.level = "INFO"  # default level
            self.log_file = log_file or os.path.join("logs", "testing_center.log")
            self.max_bytes = max_bytes
            self.backup_count = backup_count
            
            # Create logs directory if it doesn't exist
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            
            # Setup handlers
            self._setup_handlers()

    def _setup_handlers(self):
        """Setup console and file handlers with rotation"""
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler with colors
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter("%(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)
        
        # File handler with rotation and timestamps
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_file, 
            maxBytes=self.max_bytes, 
            backupCount=self.backup_count
        )
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)

    @staticmethod
    def get_instance():
        """Static access method for singleton"""
        if Logger._instance is None:
            Logger()
        return Logger._instance

    def set_level(self, level):
        """Set the logging level"""
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        self.level = level.upper()
        self.logger.setLevel(level_map.get(level.upper(), logging.INFO))
        
        # Update file handler level to match
        for handler in self.logger.handlers:
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                handler.setLevel(level_map.get(level.upper(), logging.INFO))

    def get_level(self):
        return self.level

    def configure_from_args(self, log_file=None, max_bytes=None, backup_count=None):
        """Reconfigure logger with new parameters"""
        if log_file:
            self.log_file = log_file
        if max_bytes:
            self.max_bytes = max_bytes
        if backup_count:
            self.backup_count = backup_count
        
        # Recreate logs directory if needed
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Re-setup handlers with new configuration
        self._setup_handlers()

    def debug(self, msg, *args, **kwargs):
        self.logger.debug("\033[94m" + msg + "\033[0m", *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info("\033[92m" + msg + "\033[0m", *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning("\033[93m" + msg + "\033[0m", *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error("\033[91m" + msg + "\033[0m", *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical("\033[95m" + msg + "\033[0m", *args, **kwargs)
