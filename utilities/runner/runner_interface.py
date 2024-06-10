from abc import ABC, abstractmethod

class RunnerInterface(ABC):
    @abstractmethod
    def run_test_command(self, filename, file_path, test_case_command):
        pass
