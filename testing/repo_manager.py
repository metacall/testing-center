import os
import subprocess
from testing.logger import Logger

class RepoManager:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.logger = Logger.get_instance()

    def clone_repo_if_not_exist(self):
        try:
            repo_name = self.repo_url.split('/')[-1].split('.')[0]
            if os.path.isdir(repo_name):
                self.logger.warning("Repo is already cloned!")
            else:
                process = subprocess.Popen(['git', 'clone', self.repo_url], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                _, stderr = process.communicate()
                stderr = stderr.decode('utf-8')
                error_keywords = ["Fatal", "fatal", "error", "Error", "ERROR"]
                if any(keyword in stderr for keyword in error_keywords):
                    raise ValueError(stderr)
                self.logger.debug("Repo is cloned successfully!")
        except ValueError as e:
            self.logger.error(f"Error: {e}")
            exit()
