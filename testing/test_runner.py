import re
import unittest
from testing.runner.interface_factory import InterfaceFactory
from testing.logger import Logger

class TestCaseGenerator:
    @staticmethod
    def create_test_method(interface, test_case_name, test_case_command, test_case_expected_stdout):
        def test_method(self):
            out_str = interface.run_test_command(self.file_path, test_case_command)
            passed = self.check_match(out_str, test_case_expected_stdout)
            self.assertTrue(passed, f"{interface.get_name()}_{test_case_name} - Expected: {test_case_expected_stdout}, Actual: {out_str}")
        return test_method

    @staticmethod
    def check_match(actual, expected_pattern):
        actual_cleaned = re.sub(r'\s+', ' ', actual).strip()
        expected_pattern_cleaned = re.sub(r'\s+', ' ', expected_pattern).strip()
        return bool(re.search(expected_pattern_cleaned, actual_cleaned, re.DOTALL))

class DynamicTestSuiteFactory:
    def __init__(self, logger, interfaces):
        self.logger = logger
        self.interfaces = interfaces

    def create_test_suite(self, file_path, test_cases):
        logger = self.logger

        class DynamicTestSuite(unittest.TestCase):
            @classmethod
            def setUpClass(cls):
                cls.file_path = file_path
                cls.logger = logger

            @staticmethod
            def check_match(actual, expected_pattern):
                return TestCaseGenerator.check_match(actual, expected_pattern)

        for test_case in test_cases:
            test_case_name, test_case_command, test_case_expected_stdout = test_case
            for interface in self.interfaces:
                test_method = TestCaseGenerator.create_test_method(interface, test_case_name, test_case_command, test_case_expected_stdout)
                test_method_name = f'testCase_{interface.get_name()}_{test_case_name}'
                setattr(DynamicTestSuite, test_method_name, test_method)

        return DynamicTestSuite

class TestRunner:
    def __init__(self, interface_types):
        self.logger = Logger.get_instance()
        self.interfaces = [InterfaceFactory.get_interface(interface_type) for interface_type in interface_types]
        self.test_suite_factory = DynamicTestSuiteFactory(self.logger, self.interfaces)
        self.test_verbosity = 2 if self.logger.get_level() == "DEBUG" else 1

    def create_project_test_suites(self, test_suites):
        test_loader = unittest.TestLoader()
        master_suite = unittest.TestSuite()

        for file_path, test_cases in test_suites:
            test_suite = self.test_suite_factory.create_test_suite(file_path, test_cases)
            master_suite.addTests(test_loader.loadTestsFromTestCase(test_suite))
        return master_suite

    def run_tests(self, project_name, test_suites):
        master_suite = self.create_project_test_suites(test_suites)
        runner = unittest.TextTestRunner(verbosity=self.test_verbosity)
        result = runner.run(master_suite)
        if not result.wasSuccessful():
            self.logger.error("Some tests failed!")
            exit(1)
