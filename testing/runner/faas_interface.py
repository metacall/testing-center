import json
import subprocess

import config

from testing.runner.runner_interface import RunnerInterface


class FaaSInterface(RunnerInterface):
    def __init__(self):
        self.base_url = "http://localhost:9000/9b150a863eeb"

    def get_name(self):
        return "faas"
    
    def get_request(self, url):
        command = f"curl {url} -X GET"
        return command

    def post_request(self, url, params):
        try:
            params = json.loads(params)
        except json.JSONDecodeError:
            pass

        data = json.dumps(params) if isinstance(params, dict) else params
        command = f"curl {url} -X POST --data '{data}'"
        return command


    def parse_function_call(self, function_call):
        if '(' in function_call and ')' in function_call:
            function_name = function_call.split('(')[0]
            params = function_call.split('(')[1].split(')')[0]
            params = params if params else None
        else:
            function_name = function_call
            params = None

        return function_name, params
    
    def run_test_command(self, file_path, function_call):
        function_name, params = self.parse_function_call(function_call)
        url = f"{self.base_url}/{config.project_name}/v1/call/{function_name}"

        if params:
            command = self.post_request(url, params)
        else:
            command = self.get_request(url)
        print("Command:", command)

        result = subprocess.run(command, capture_output=True, text=True, shell=True, check=False)
        out_str = result.stdout.strip()

        return out_str
