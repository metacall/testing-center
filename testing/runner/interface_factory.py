from testing.runner.cli_interface import CLIInterface
from testing.runner.faas_interface import FaaSInterface

class InterfaceFactory:
    @staticmethod
    def get_interface(interface_type):
        if interface_type == "cli":
            return CLIInterface()
        elif interface_type == "faas":
            return FaaSInterface()
        else:
            raise ValueError(f"Unknown interface type: {interface_type}")
