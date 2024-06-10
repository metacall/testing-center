import subprocess
from utilities.runner.runner_interface import RunnerInterface
from utilities.logger import Logger

class CLIInterface(RunnerInterface):
    def __init__(self):
        self.logger = Logger.get_instance()

    def get_runtime_tag(self, file_name):
        file_extension = file_name.split('.')[-1]
        runtime_tags = {
            'py': 'py',
            'js': 'node',
            'rb': 'rb',
            'cs': 'cs',
            'cob': 'cob',
            'ts': 'ts'
        }
        if file_extension in runtime_tags:
            return runtime_tags[file_extension]
        else:
            raise ValueError("Error: file extension not supported!")
        
    def run_test_command(self, filename, file_path, test_case_command):
        try:
            process = subprocess.Popen(['metacall'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.logger.debug("Metacall CLI started...")
            

            commands = ['load ' + ' ' + self.get_runtime_tag(filename) + ' ' + file_path, test_case_command, 'exit']
            commands = '\n'.join(commands) + '\n' # join the commands with a newline character

            process.stdin.write(f"{commands}".encode('utf-8'))
            process.stdin.flush()
            
            stdout, _ = process.communicate()
            out_str = stdout.decode('utf-8').strip().split('λ')
            out_str = out_str[2]
            return out_str
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return None
