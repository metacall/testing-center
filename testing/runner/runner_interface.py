from abc import ABC, abstractmethod

class RunnerInterface(ABC):
    @abstractmethod
    def run_test_command(self, file_path, functionCall):
        pass
