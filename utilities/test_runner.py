import re
from utilities.runner.interface_factory import InterfaceFactory
from utilities.logger import Logger

class TestRunner:
    def __init__(self, interface_type):
        self.interface = InterfaceFactory.get_interface(interface_type)
        self.logger = Logger.get_instance()

    def run_tests(self, project_name, test_suites):
        self.logger.info(f"{project_name}\n================================")
        for file_path, test_cases in test_suites:
            file_name = file_path.split('/')[-1]

            self.logger.info(f"{file_name}\n=============")
            for test_case_order, test_case in enumerate(test_cases):
                test_case_name, test_case_command, test_case_expected_stdout = test_case
                self.logger.debug(f"{test_case_order}. Test Case Command: {test_case_command}")

                results = self.interface.run_test_command(file_name, file_path, test_case_command)

                all_passed = True
                for runner_name, out_str in results.items():

                    passed = self.check_output(out_str, test_case_expected_stdout)
                    self.logger.info(f"{runner_name} - Test Case: {test_case_name} {'PASSED' if passed else 'FAILED'}")
                    if not passed:
                        all_passed = False
                        self.logger.debug(f"{runner_name} - Expected: {test_case_expected_stdout}")
                        self.logger.debug(f"{runner_name} - Actual: {out_str}")

                self.logger.info(f"Overall Test Case: {test_case_name} {'PASSED' if all_passed else 'FAILED'}")

    def check_output(self, actual, expected_pattern):
        actual_cleaned = re.sub(r'\s+', ' ', actual).strip()
        expected_pattern_cleaned = re.sub(r'\s+', ' ', expected_pattern).strip()
        return bool(re.search(expected_pattern_cleaned, actual_cleaned, re.DOTALL))
