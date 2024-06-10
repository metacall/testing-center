import os
import subprocess
from utilities.logger import Logger

class RepoManager:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.logger = Logger.get_instance()

    def clone_repo_if_not_exist(self):
        try:
            repo_name = self.repo_url.split('/')[-1].split('.')[0]
            if os.path.isdir(repo_name):
                self.logger.debug("Repo is already cloned!")
            else:
                process = subprocess.Popen(['git', 'clone', self.repo_url], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                _, stderr = process.communicate()
                stderr = stderr.decode('utf-8')
                if "Fatal" in stderr or "fatal" in stderr or "error" in stderr or "Error" in stderr or "ERROR" in stderr:
                    raise Exception(stderr)
                self.logger.debug("Repo is cloned successfully!")
        except Exception as e:
            self.logger.error(f"Error: {e}")
            exit()
