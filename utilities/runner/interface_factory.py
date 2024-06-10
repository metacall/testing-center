from utilities.runner.cli_interface import CLIInterface
from utilities.runner.faas_interface import FaaSInterface
from utilities.runner.composite_runner_interface import CompositeRunnerInterface

class InterfaceFactory:
    @staticmethod
    def get_interface(interface_type):
        if interface_type == "cli":
            return CLIInterface()
        elif interface_type == "faas":
            return FaaSInterface()
        elif interface_type == "composite":
            composite = CompositeRunnerInterface()
            composite.add_runner(CLIInterface())
            composite.add_runner(FaaSInterface())
            return composite
        else:
            raise ValueError(f"Unknown interface type: {interface_type}")
