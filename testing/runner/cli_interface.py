import platform
import subprocess
from testing.runner.runner_interface import RunnerInterface
from testing.logger import Logger


class CLIInterface(RunnerInterface):
    """Interface for the CLI runner"""

    def __init__(self, logger=None):
        self.logger = logger or Logger.get_instance()

    def get_name(self):
        """Get the name of the interface"""
        return "cli"

    def get_runtime_tag(self, file_name):
        """Get the runtime tag for the file extension"""
        file_extension = file_name.split(".")[-1]
        runtime_tags = {
            "py": "py",
            "js": "node",
            "rb": "rb",
            "cs": "cs",
            "cob": "cob",
            "ts": "ts",
        }
        if file_extension in runtime_tags:
            return runtime_tags[file_extension]
        else:
            raise ValueError("Error: file extension not supported!")

    def get_test_command(self, file_path, function_call):
        """Get the test command for the test case"""
        file_name = file_path.split("/")[-1]
        function_call = "call " + function_call
        command = [
            "load " + " " + self.get_runtime_tag(file_name) + " " + file_path,
            function_call,
            "exit",
        ]
        return "\n".join(command) + "\n"  # join the commands with a newline character

    def run_test_command(self, file_path, function_call):
        """Run the test command"""
        try:
            command = self.get_test_command(file_path, function_call)

            process_cmd = (
                ["metacall.bat"] if platform.system() == "Windows" else ["metacall"]
            )
            process = subprocess.Popen(
                process_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            process.stdin.write(command.encode("utf-8"))
            process.stdin.flush()

            stdout, _ = process.communicate()
            out_str = (
                stdout.decode("utf-8")
                .strip()
                .split("\n>" if platform.system() == "Windows" else "λ")
            )

            return out_str[2]

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error: {e}")
            return None
