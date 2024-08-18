import logging


class Logger:
    """Singleton class to manage the logging"""

    _instance = None

    def __init__(self):
        if Logger._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Logger._instance = self
            self.logger = logging.getLogger("CLI_Tool")
            self.level = "INFO"  # default level
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
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

    def get_level(self):
        return self.level

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
