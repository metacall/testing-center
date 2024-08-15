import os
import subprocess
import json
from testing.logger import Logger

class DeployManager:
    _instance = None

    def __init__(self, project_path):
        if DeployManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DeployManager._instance = self
        self.logger = Logger.get_instance()
        self.project_path = project_path
        self.project_name = project_path.rsplit('/', maxsplit=1)[-1]
    
    @staticmethod
    def get_instance():
        ''' Static access method for singleton '''
        if DeployManager._instance is None:
            DeployManager(None)
        return DeployManager._instance
    
    def deploy_local_faas(self):
        ''' Deploy the project as a local faas '''
        # Set the environment variables
        try:
            os.environ['NODE_ENV'] = 'testing'
            os.environ['METACALL_DEPLOY_INTERACTIVE'] = 'false'
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error setting the environment variables: {e}")
            return False
        # Deploy the project
        try:
            deploy_command = f"metacall-deploy --dev --workdir {self.project_path}"
            _ = subprocess.run(deploy_command, capture_output=True, text=True, shell=True, check=False)
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error deploying the project: {e}")
            return False

    def get_local_base_url(self):
        ''' Get the base url of the deployed local faas '''
        inspection_command = "metacall-deploy --inspect OpenAPIv3 --dev"
        # Inspect the deployed project
        result = subprocess.run(inspection_command, capture_output=True, text=True, shell=True, check=False)
        # Parse the JSON output to get the server URL and paths
        try:
            server_url = json.loads(result.stdout)[0]['servers'][0]['url']
        except json.JSONDecodeError:
            self.logger.error(f"Error parsing JSON output: {result.stderr}")
            return None
        self.logger.debug(f"Local faas base url: {server_url}")
        return server_url # e.g. http://localhost:9000/aee940974fd5/examples-testing/v1

    def deploy_remote_faas(self):
        ''' Deploy the project as a remote faas '''
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