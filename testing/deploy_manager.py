import os
import subprocess
import json
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
        ''' Static access method for singleton '''
        if DeployManager._instance is None:
            if project_path is None:
                raise ValueError("Project path must be provided for the first instance.")
            DeployManager(project_path)
        return DeployManager._instance

    def set_environment_variables(self, env_vars):
        ''' Set environment variables '''
        try:
            for key, value in env_vars.items():
                os.environ[key] = value
        except Exception as e:
            self.logger.error(f"Error setting environment variables: {e}")
            return False
        return True

    def deploy_local_faas(self):
        ''' Deploy the project as a local FaaS '''
        env_vars = {
            'NODE_ENV': 'testing',
            'METACALL_DEPLOY_INTERACTIVE': 'false'
        }

        if not self.set_environment_variables(env_vars):
            return False

        try:
            deploy_command = f"metacall-deploy --dev --workdir {self.project_path}"
            subprocess.run(deploy_command, capture_output=True, text=True, shell=True, check=True)
            self.logger.debug("Local FaaS deployed successfully.")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error deploying the project: {e}")
            return False

    def get_local_base_url(self):
        ''' Get the base URL of the deployed local FaaS '''
        inspection_command = "metacall-deploy --inspect OpenAPIv3 --dev"
        try:
            result = subprocess.run(inspection_command, capture_output=True, text=True, shell=True, check=True)
            server_url = json.loads(result.stdout)[0]['servers'][0]['url']
            self.logger.debug(f"Local FaaS base URL: {server_url}")
            return server_url
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error inspecting the deployed project: {e}")
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Error parsing JSON output: {e}")
        return None

    def deploy_remote_faas(self):
        ''' Deploy the project as a remote FaaS '''
        pass

    def get_remote_base_url(self):
        ''' Get the base url of the deployed remote faas '''

'''
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

'''