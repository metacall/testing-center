import os
import subprocess
from testing.logger import Logger


class RepoManager:
    """Singleton class to manage the repositories"""

    _instance = None

    def __init__(self, repo_url):
        if RepoManager._instance is not None:
            raise Exception("This class is a singleton!")
        RepoManager._instance = self

        self.repo_url = repo_url
        self.logger = Logger.get_instance()

    @staticmethod
    def get_instance(repo_url=None):
        """Static access method for singleton"""
        if RepoManager._instance is None:
            if repo_url is None:
                raise ValueError(
                    "Repository URL must be provided for the first instance."
                )
            RepoManager(repo_url)
        return RepoManager._instance

    def repo_exists(self, repo_name):
        """Check if the repository already exists"""
        return os.path.isdir(repo_name)

    def clone_repo_if_not_exist(self):
        """Clone the repository if not already cloned"""
        repo_name = self.repo_url.split("/")[-1].split(".")[0]

        if self.repo_exists(repo_name):
            self.logger.warning("Repository is already cloned!")
            return

        try:
            command = f"git clone {self.repo_url}"
            result = subprocess.run(
                command, capture_output=True, text=True, shell=True, check=False
            )

            if "fatal" in result.stderr.lower():
                raise ValueError(result.stderr)

            self.logger.debug("Repository cloned successfully!")
        except ValueError as e:
            self.logger.error(f"Error cloning the repository: {e}")
            raise
