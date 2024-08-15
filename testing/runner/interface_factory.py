from testing.logger import Logger
from testing.runner.cli_interface import CLIInterface
from testing.runner.faas_interface import FaaSInterface

class InterfaceFactory:
    ''' Factory class to create interfaces '''

    @staticmethod
    def get_interface(interface_type):
        ''' Get the interface based on the type '''
        logger = Logger.get_instance()
        if interface_type == "cli":
            return CLIInterface(logger)
        elif interface_type == "faas":
            return FaaSInterface(logger)
        else:
            logger.error(f"Unknown interface type: {interface_type}")
            raise ValueError(f"Unknown interface type: {interface_type}")
