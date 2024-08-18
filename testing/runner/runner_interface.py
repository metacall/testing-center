from abc import ABC, abstractmethod


class RunnerInterface(ABC):
    """Interface for the runner classes"""

    @abstractmethod
    def run_test_command(self, file_path, function_call):
        """Run the test command"""

    @abstractmethod
    def get_test_command(self, file_path, function_call):
        """Get the test command"""

    @abstractmethod
    def get_name(self):
        """Get the name of the interface"""
