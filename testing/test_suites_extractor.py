import yaml
from testing.logger import Logger

class TestSuitesExtractor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.logger = Logger.get_instance()

    def extract_test_suites(self):
        try:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        except FileNotFoundError:
            self.logger.error(f"Error: file ({self.file_name}) does not exist!")
            exit()

        try:
            project_name = data['project']
            repo_url = data['repo-url']
            code_files = data['code-files']
            test_suites = []
            for code_file in code_files:
                test_cases = [(test_case['name'], test_case['command'], test_case['expected-stdout']) for test_case in code_file['test-cases']]
                test_suites.append((code_file['path'], test_cases))
        except KeyError as e:
            self.logger.error(f"Error: parsing yaml file, missing key:{e}")
            exit()
        return project_name, repo_url, test_suites
