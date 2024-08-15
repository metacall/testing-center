import os
import subprocess
import json
from testing.logger import Logger

class DeployManager:
    _instance = None

    @staticmethod
    def get_instance():
        if DeployManager._instance is None:
            DeployManager()
        return DeployManager._instance
    def __init__(self, project_path):
        if DeployManager._instance is not None:
            raise SingletonException("This class is a singleton!")
        else:
            DeployManager._instance = self
        self.logger = Logger.get_instance()
        self.project_path = project_path
        self.project_name = project_path.split('/')[-1]
    
    def deploy_local_faas(self):
        os.environ['NODE_ENV'] = 'testing'
        os.environ['METACALL_DEPLOY_INTERACTIVE'] = 'false'
        try:
          deploy_command = f"metacall-deploy --dev --workdir {self.project_path}"
          _ = subprocess.run(deploy_command, capture_output=True, text=True, shell=True, check=False)
          return True
        except Exception as e:
          self.logger.error(f"Error deploying the project: {e}")
          return False

    def get_local_base_url(self):
        inspection_command = f"metacall-deploy --inspect OpenAPIv3 --dev"
        result = subprocess.run(inspection_command, capture_output=True, text=True, shell=True, check=False)
        # Parse the JSON output to get the server URL and paths
        try:
          server_url = json.loads(result.stdout)[0]['servers'][0]['url']
        except json.JSONDecodeError:
          self.logger.error(f"Error parsing JSON output: {result.stdout}")
          return None
        # paths = json.loads(result.stdout)[0]['paths'] # e.g. http://localhost:9000/aee940974fd5/examples-testing/v1/call/index
        self.logger.debug(f"Local faas base url: {server_url}")
        return server_url # e.g. http://localhost:9000/aee940974fd5/examples-testing/v1


    def deploy_remote_faas(self):
        pass
    def get_remote_base_url(self):
        pass

'''
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