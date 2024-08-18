import argparse

from testing.logger import Logger
from testing.repo_manager import RepoManager
from testing.deploy_manager import DeployManager
from testing.test_runner import TestRunner
from testing.test_suites_extractor import TestSuitesExtractor


def parse_arguments():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser(
        description="Run test suites in specified environments."
    )
    parser.add_argument("-f", "--file", required=True, help="The test suite file name.")
    parser.add_argument(
        "-V", "--verbose", action="store_true", help="Increase output verbosity."
    )
    parser.add_argument(
        "-e",
        "--envs",
        nargs="+",
        default=["cli"],
        help="Environments to run the tests on (cli, faas).",
    )
    return parser.parse_args()


def setup_logger(verbose):
    """Setup logger with the appropriate logging level"""
    logger = Logger.get_instance()
    logger.set_level("DEBUG" if verbose else "INFO")
    return logger


def extract_test_suites(file_name):
    """Extract test suites from the test suite file"""
    try:
        test_suites_extractor = TestSuitesExtractor(file_name)
        return test_suites_extractor.extract_test_suites()
    except Exception as e:
        raise RuntimeError(f"Error extracting test suites: {e}")


def clone_repo_if_needed(repo_url):
    """Clone the repository if not already cloned"""
    try:
        repo_manager = RepoManager.get_instance(repo_url)
        repo_manager.clone_repo_if_not_exist()
    except Exception as e:
        raise RuntimeError(f"Error cloning repository: {e}")


def deploy_faas_if_needed(envs, project_path, logger):
    """Deploy the project as a local FaaS if required"""
    if "faas" in envs:
        deploy_manager = DeployManager.get_instance(project_path)
        if not deploy_manager.deploy_local_faas():
            logger.error(
                "Error deploying the project. Removing 'faas' from environments."
            )
            envs.remove("faas")


def run_tests(envs, test_suites):
    """Run the tests in the specified environments"""
    test_runner = TestRunner(envs)
    test_runner.run_tests(test_suites)


def main():
    args = parse_arguments()
    logger = setup_logger(args.verbose)

    try:
        project_name, project_path, repo_url, test_suites = extract_test_suites(
            args.file
        )
        logger.info(f"Testing Project: {project_name}")

        clone_repo_if_needed(repo_url)
        deploy_faas_if_needed(args.envs, project_path, logger)
        run_tests(args.envs, test_suites)

    except RuntimeError as e:
        logger.error(e)
        exit(1)


if __name__ == "__main__":
    main()
