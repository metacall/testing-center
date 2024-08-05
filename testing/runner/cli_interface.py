import platform
import subprocess
from testing.runner.runner_interface import RunnerInterface
from testing.logger import Logger

class CLIInterface(RunnerInterface):
    def __init__(self):
        self.logger = Logger.get_instance()
    def get_name(self):
        return "cli"

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
        
    def run_test_command(self, file_path, functionCall):
        file_name = file_path.split('/')[-1]
        functionCall = 'call ' + functionCall
        try:
            if platform.system() == 'Windows':
                process = subprocess.Popen(['metacall.bat'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                process = subprocess.Popen(['metacall'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            commands = ['load ' + ' ' + self.get_runtime_tag(file_name) + ' ' + file_path, functionCall, 'exit']
            commands = '\n'.join(commands) + '\n' # join the commands with a newline character
        
            process.stdin.write(f"{commands}".encode('utf-8'))
            process.stdin.flush()
            
            stdout, _ = process.communicate()
            
            out_str = stdout.decode('utf-8').strip().split('\n>' if platform.system() == 'Windows' else 'λ')
            return out_str[2]
        
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error: {e}")
            return ""
