import os
import subprocess
import json
import time
import platform
from testing.logger import Logger


class DeployManager:
    _instance = None

    def __init__(self, project_path):
        if DeployManager._instance is not None:
            raise Exception("This class is a singleton!")
        DeployManager._instance = self

        self.logger = Logger.get_instance()
        self.project_path = project_path
        self.project_name = os.path.basename(project_path)

    @staticmethod
    def get_instance(project_path=None):
        """Static access method for singleton"""
        if DeployManager._instance is None:
            if project_path is None:
                raise ValueError(
                    "Project path must be provided for the first instance."
                )
            DeployManager(project_path)
        return DeployManager._instance

    def set_environment_variables(self, env_vars):
        """Set environment variables"""
        try:
            for key, value in env_vars.items():
                os.environ[key] = value
        except Exception as e:
            self.logger.error(f"Error setting environment variables: {e}")
            return False
        return True

    def _run_command(self, command):
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True,
            check=True,
        )

    def deploy_local_faas(self):
        """Deploy the project as a local FaaS"""
        env_vars = {
            "NODE_ENV": "testing",
            "METACALL_DEPLOY_INTERACTIVE": "false",
        }

        if not self.set_environment_variables(env_vars):
            return False

        base_command = "metacall deploy --dev --workdir "
        deploy_command = base_command + self.project_path
        inspection_command = "metacall deploy --inspect OpenAPIv3 --dev"
        max_retries = 3

        for attempt in range(1, max_retries + 1):
            try:
                self._run_command(deploy_command)
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Error deploying the project: {e}")
                time.sleep(10)
                continue

            try:
                result = self._run_command(inspection_command)
            except subprocess.CalledProcessError as e:
                self.logger.error("Error inspecting deploy: %s" % e)
                time.sleep(10)
                continue

            stdout = result.stdout
            if platform.system() == "Windows":
                # metacall.bat echoes the command line before JSON output.
                stdout_lines = stdout.splitlines()
                stdout = "\n".join(stdout_lines[1:]) if stdout_lines else ""
            try:
                parsed = json.loads(stdout)
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                self.logger.error(f"Error parsing JSON output: {e}")
                time.sleep(10)
                continue
            if isinstance(parsed, list) and parsed:
                self.logger.debug("Local FaaS deployed successfully.")
                return True

            self.logger.error("Deploy inspection returned empty result.")
            time.sleep(10)

        return False

    def get_local_base_url(self):
        """Get the base URL of the deployed local FaaS"""
        inspection_command = "metacall deploy --inspect OpenAPIv3 --dev"
        max_retries = 20
        for attempt in range(1, max_retries + 1):
            try:
                result = self._run_command(inspection_command)
            except subprocess.CalledProcessError as e:
                self.logger.error("Error inspecting deployed project: %s" % e)
                time.sleep(10)
                continue

            stdout = result.stdout
            self.logger.debug(f"Inspect stdout (raw): {stdout}")
            if platform.system() == "Windows":
                # metacall.bat echoes the command line before JSON output.
                stdout_lines = stdout.splitlines()
                stdout = "\n".join(stdout_lines[1:]) if stdout_lines else ""
            self.logger.debug(f"Inspect stdout (extracted): {stdout}")

            try:
                parsed = json.loads(stdout)
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                self.logger.error(f"Error parsing JSON output: {e}")
                time.sleep(10)
                continue

            self.logger.debug(f"Inspect JSON (parsed): {parsed}")
            if not isinstance(parsed, list) or not parsed:
                self.logger.error("Unexpected JSON: empty list.")
                time.sleep(10)
                continue
            first_entry = parsed[0]
            if not isinstance(first_entry, dict):
                self.logger.error("Unexpected JSON: item is not an object.")
                time.sleep(10)
                continue
            servers = first_entry.get("servers")
            if not isinstance(servers, list) or not servers:
                self.logger.error("Unexpected JSON: missing servers list.")
                time.sleep(10)
                continue
            first_server = servers[0]
            if not isinstance(first_server, dict) or "url" not in first_server:
                self.logger.error("Unexpected JSON: missing servers[0].url.")
                time.sleep(10)
                continue
            server_url = first_server["url"]
            self.logger.debug(f"Local FaaS base URL: {server_url}")
            return server_url

        return None

    def deploy_remote_faas(self):
        """Deploy the project as a remote FaaS"""
        pass

    def get_remote_base_url(self):
        """Get the base url of the deployed remote faas"""


"""
Paths: http://localhost:9000/aee940974fd5/examples-testing/v1/call/index
Exmaple output
[
  {
    "openapi": "3.0.0",
    "info": {
      "title": "MetaCall Cloud FaaS deployment 'time-app-web'",
      "description": "",
      "version": "v1"
    },
    "servers": [
      {
        "url": "http://localhost:9000/aa759149a70a/time-app-web/v1",
        "description": "MetaCall Cloud FaaS"
      }
    ],
    "paths": {
      "/call/time": {
        "get": {
          "summary": "",
          "description": "",
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {}
                }
              }
            }
          }
        }
      },
      "/call/index": {
        "get": {
          "summary": "",
          "description": "",
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {}
                }
              }
            }
          }
        }
      }
    }
  }
]

"""
