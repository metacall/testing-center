# MetaCall Test Center

## Overview

MetaCall Test Center is a comprehensive testing framework designed for MetaCall projects and examples. It provides a structured and efficient way to define, run, and manage test cases across different environments. The primary script, `testing.py`, integrates seamlessly into CI/CD pipelines and supports local testing. This project adheres to best practices, SOLID principles, and design patterns to ensure maintainability, scalability, and ease of contribution.

## Project Structure

The project is organized as follows:

``` bash
.
├── README.md
├── LICENSE
├── requirements.txt
├── testing
│   ├── __init__.py
│   ├── deploy_manager.py
│   ├── logger.py
│   ├── repo_manager.py
│   ├── runner
│   │   ├── cli_interface.py
│   │   ├── faas_interface.py
│   │   ├── interface_factory.py
│   │   └── runner_interface.py
│   ├── test_runner.py
│   └── test_suites_extractor.py
├── testing.py
└── test-suites
    └── test<example name>.yaml  
```

### Components

- **`testing.py`**: The main script that orchestrates the testing process by interacting with various components.
  
- **`deploy_manager.py`**: Manages the deployment of MetaCall projects locally or remotely, ensuring the necessary environments are set up for testing.

- **`logger.py`**: Provides a centralized logging mechanism with configurable verbosity levels, helping to debug and monitor the testing process.

- **`repo_manager.py`**: Handles cloning and managing the code repositories required for testing, ensuring that the latest code is always used.

- **`test_runner.py`**: The core component responsible for executing test cases across different environments by leveraging the strategy pattern for flexibility.

- **`test_suites_extractor.py`**: Extracts test cases from YAML files, ensuring that the test cases are correctly parsed and ready for execution.

- **`runner`**: Contains specific implementations for running tests in different environments:
  - **`runner_interface.py`**: Defines the interface for all runner implementations, adhering to the Dependency Inversion principle.
  - **`cli_interface.py`**: Implements the interface for running tests in a CLI environment.
  - **`faas_interface.py`**: Implements the interface for running tests in a Function-as-a-Service (FaaS) environment.
  - **`interface_factory.py`**: A factory class that creates instances of the appropriate runner interface based on the environment.

## How It Works

1. **Test Suite Definition**: Test cases are defined in YAML format within the `test-suites` directory. Each test suite specifies the project, repository URL, code files, and individual test cases.

2. **Test Execution**: The `testing.py` script is executed with various command-line arguments. The script then:
   - Parses the command-line arguments.
   - Extracts test cases from the specified YAML file.
   - Clones the repository if not already present.
   - Deploys the project as a local FaaS (if required).
   - Runs the test cases across the specified environments (CLI, FaaS, etc.).

3. **Output and Logging**: The results of the test cases are logged based on the specified verbosity level, and any errors encountered during the process are reported.

## Design Choices and Principles

This project adheres to several key design principles and patterns:

- **SOLID Principles**:
  - **Single Responsibility Principle**: Each class has a single responsibility, making the code easier to understand and maintain.
  - **Open/Closed Principle**: The code is open for extension but closed for modification. New runner environments can be added without modifying existing code.
  - **Liskov Substitution Principle**: Subtypes (`CLIInterface`, `FaaSInterface`) can be used interchangeably with their base type (`RunnerInterface`) without affecting the correctness of the program.
  - **Interface Segregation Principle**: The `RunnerInterface` provides a minimal set of methods required by all runner types, preventing unnecessary dependencies.
  - **Dependency Inversion Principle**: High-level modules (e.g., `TestRunner`) do not depend on low-level modules (`CLIInterface`, `FaaSInterface`), but both depend on abstractions (`RunnerInterface`).

- **Design Patterns**:
  - **Factory Pattern**: The `InterfaceFactory` class encapsulates the creation of runner interfaces, promoting flexibility and adherence to the Open/Closed Principle.
  - **Singleton Pattern**: The `DeployManager` and `RepoManager` classes are implemented as singletons to ensure that only one instance exists throughout the application, avoiding redundant deployments or repository clones.
  - **Strategy Pattern**: The `TestRunner` uses different strategies (`CLIInterface`, `FaaSInterface`) to run tests in various environments, making the code flexible and easy to extend.

## Usage

### Test Suite Format

Test suites are written in YAML format. Below is an example:

```yaml
project: random-password-generator-example
repo-url: https://github.com/metacall/random-password-generator-example
code-files:
  - path: random-password-generator-example/app.py
    test-cases:
      - name: Check the password is generated in the correct length
        function-call: getRandomPassword(12)
        expected-pattern: '\"[\w\W]{12}\"'
      - name: Check the password is generated in the correct length
        function-call: getRandomPassword()
        expected-pattern: 'missing 1 required positional argument'
```

### Running Tests

To run the tests, use the following command:

```bash
python3 ./testing.py -f <test-suite-file> -V -e <environments>
```

- `-f`, `--file`: Specifies the test suite file name.
- `-V`, `--verbose`: Increases output verbosity.
- `-e`, `--envs`: Specifies the environments to run the tests on (e.g., `cli`, `faas`).

Example:

```bash
python3 ./testing.py -f test-suites/test-time-app-web.yaml -V -e cli faas
```

## Contributing

We welcome contributions to the MetaCall Test Center! Here are a few ways you can help improve the project:

- **Enhance Test Coverage**: Add new test cases or improve existing ones to cover more scenarios.
- **Optimize Code**: Refactor and optimize the codebase to improve performance and readability.
- **Extend Functionality**: Implement support for additional environments or enhance existing ones.
- **Documentation**: Improve and expand the documentation to help new users and contributors.

### Guidelines

- Follow the existing code style and structure.
- Ensure that all tests pass before submitting a pull request.
- Provide clear and concise commit messages.
- Open an issue to discuss potential changes before submitting significant modifications.
