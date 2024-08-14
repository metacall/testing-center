import argparse

import config

from testing.logger import Logger
from testing.repo_manager import RepoManager
from testing.deploy_manager import DeployManager
from testing.test_runner import TestRunner
from testing.test_suites_extractor import TestSuitesExtractor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", action="store", help="the test suite file name")
    parser.add_argument("-V", "--verbose", action="store_true", help="increase output verbosity")
    parser.add_argument("-e", "--environments", nargs="+", default=["cli"], help="the environments to run the tests")
    args = parser.parse_args()

    logger = Logger.get_instance()
    if args.verbose:
        logger.set_level("DEBUG")
    else:
        logger.set_level("INFO")

    test_suite_file_name = args.file
    if not test_suite_file_name:
        logger.error("Error: test suite file name is required!")


    test_suites_extractor = TestSuitesExtractor(test_suite_file_name)
    project_path, repo_url, test_suites = test_suites_extractor.extract_test_suites()
    project_name = project_path.split('/')[-1]
    logger.info(f"Testing Project: {project_name}")
                
    repo_manager = RepoManager(repo_url)
    repo_manager.clone_repo_if_not_exist()

    if "faas" in args.environments:
        deploy_manager = DeployManager(project_path)
        if deploy_manager.deploy_local_faas() == False:
            logger.error("Error deploying the project, remove faas from the environments")
            args.environments.remove("faas")
            
    test_runner = TestRunner(args.environments)
    test_runner.run_tests(test_suites)

if __name__ == "__main__":
    main()
