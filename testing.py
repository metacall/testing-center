import argparse
from testing.repo_manager import RepoManager
from testing.test_suites_extractor import TestSuitesExtractor
from testing.test_runner import TestRunner
from testing.logger import Logger

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", action="store", help="the test suite file name")
    parser.add_argument("-V", "--verbose", action="store_true", help="increase output verbosity")
    args = parser.parse_args()

    logger = Logger.get_instance()
    if args.verbose:
        logger.set_level("DEBUG")
    else:
        logger.set_level("INFO")

    test_suite_file_name = args.file



    test_suites_extractor = TestSuitesExtractor(test_suite_file_name)
    project_name, repo_url, test_suites = test_suites_extractor.extract_test_suites()

    logger.info(f"Project: {project_name}")
                
    repo_manager = RepoManager(repo_url)
    repo_manager.clone_repo_if_not_exist()

    test_runner = TestRunner(["cli"])
    test_runner.run_tests(project_name, test_suites)

if __name__ == "__main__":
    main()
