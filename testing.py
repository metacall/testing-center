import argparse

from testing.logger import Logger
from testing.repo_manager import RepoManager
from testing.deploy_manager import DeployManager
from testing.test_runner import TestRunner
from testing.test_suites_extractor import TestSuitesExtractor


def main():

    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", action="store", help="the test suite file name")
    parser.add_argument("-V", "--verbose", action="store_true", help="increase output verbosity")
    parser.add_argument("-e", "--envs", nargs="+", default=["cli"], help="the environments to run the tests on (cli, faas)")
    args = parser.parse_args()

    # Set the logger level
    logger = Logger.get_instance()
    logger.set_level("DEBUG" if args.verbose else "INFO")

    # Extract the test suites from the test suite file
    try:
        test_suite_file_name = args.file
        test_suites_extractor = TestSuitesExtractor(test_suite_file_name)
        _, project_path, repo_url, test_suites = test_suites_extractor.extract_test_suites()
        project_name = project_path.rsplit('/', maxsplit=1)[-1]
        logger.info(f"Testing Project: {project_name}")
    except Exception as e:
        logger.error(f"Error: {e}")
        exit(1)
                  
    # Clone the repo if not already cloned
    try:
        repo_manager = RepoManager(repo_url)
        repo_manager.clone_repo_if_not_exist()
    except Exception as e:
        logger.error(f"Error: {e}")
        exit(1)

    # Deploy the project as a local faas
    if "faas" in args.envs:
        deploy_manager = DeployManager(project_path)
        if deploy_manager.deploy_local_faas() is False:
            logger.error("Error deploying the project, remove faas from the envs")
            args.envs.remove("faas")
            
    # Run the tests
    test_runner = TestRunner(args.envs)
    test_runner.run_tests(test_suites)

if __name__ == "__main__":
    main()
