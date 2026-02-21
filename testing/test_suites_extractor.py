import yaml
import os
from testing.logger import Logger
import jsonschema


class TestSuitesExtractor:
    """Singleton class to extract the test suites from the yaml file"""

    _instance = None

    # Schema definition for YAML validation
    YAML_SCHEMA = {
        "type": "object",
        "required": ["project", "repo-url", "code-files"],
        "properties": {
            "project": {"type": "string"},
            "repo-url": {"type": "string"},
            "code-files": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["path", "test-cases"],
                    "properties": {
                        "path": {"type": "string"},
                        "test-cases": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["name", "function-call", "expected-pattern"],
                                "properties": {
                                    "name": {"type": "string"},
                                    "function-call": {"type": "string"},
                                    "expected-pattern": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    def __init__(self, file_name):
        if TestSuitesExtractor._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            TestSuitesExtractor._instance = self
            self.file_name = file_name
            self.logger = Logger.get_instance()

    @staticmethod
    def get_instance():
        """Static access method for singleton"""
        if TestSuitesExtractor._instance is None:
            TestSuitesExtractor(None)
        return TestSuitesExtractor._instance

    def extract_test_suites(self):
        """Load the data from the yaml file and extract the test suites"""
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.error(f"Error: file ({self.file_name}) does not exist!")
            raise FileNotFoundError(f"Error: file ({self.file_name}) does not exist!")
        except yaml.YAMLError as e:
            self.logger.error(f"Error: parsing yaml file, {e}")
            raise yaml.YAMLError(f"Error: parsing yaml file, {e}")

        # Validate YAML structure against schema
        try:
            jsonschema.validate(data, self.YAML_SCHEMA)
        except jsonschema.ValidationError as e:
            self.logger.error(f"Error: YAML validation failed - {e.message}")
            raise ValueError(f"Invalid YAML structure: {e.message}")

        try:
            project_name = data["project"]
            repo_url = data["repo-url"]
            code_files = data["code-files"]
            project_path = os.path.dirname(code_files[0]["path"])
            test_suites = []
            for code_file in code_files:
                test_cases = [
                    (
                        test_case["name"],
                        test_case["function-call"],
                        test_case["expected-pattern"],
                    )
                    for test_case in code_file["test-cases"]
                ]
                test_suites.append((code_file["path"], test_cases))
        except KeyError as e:
            self.logger.error(f"Error: parsing yaml file, missing key:{e}")
            raise KeyError(f"Error: parsing yaml file, missing key:{e}")
        return project_name, project_path, repo_url, test_suites
