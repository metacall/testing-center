import json
import subprocess

import os

from testing.runner.runner_interface import RunnerInterface
from testing.logger import Logger
from testing.deploy_manager import DeployManager


class FaaSInterface(RunnerInterface):
    def __init__(self):
        self.logger = Logger.get_instance()
        self.deploy_manager = DeployManager.get_instance()
        self.base_url = self.deploy_manager.get_local_base_url()
        if not self.base_url:
            self.logger.error("FaaSInterface: Could not get base url")

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
        command = f"curl -X POST --data '{data}' {url} "
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
    def get_test_command(self, _, function_call):
        function_name, params = self.parse_function_call(function_call)
        url = f'{self.base_url}/call/{function_name}'

        if params:
           return self.post_request(url, params)
        else:
            return self.get_request(url)

    
    def run_test_command(self, base_url, function_call):
        command = self.get_test_command(base_url, function_call)

        result = subprocess.run(command, capture_output=True, text=True, shell=True, check=False)
        out_str = result.stdout.strip()

        return out_str
