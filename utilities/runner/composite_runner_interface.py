from utilities.runner.runner_interface import RunnerInterface

class CompositeRunnerInterface(RunnerInterface):
    def __init__(self):
        self.runners = []

    def add_runner(self, runner):
        self.runners.append(runner)

    def run_test_command(self, filename, file_path, test_case_command):
        results = {}
        for runner in self.runners:
            runner_name = type(runner).__name__
            results[runner_name] = runner.run_test_command(filename, file_path, test_case_command)
        return results
