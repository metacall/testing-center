import argparse
import yaml
import os
import subprocess
import re

# Command line argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", action="store", help="the test suite file name")
args = parser.parse_args()

def check_if_file_exists(file_path):
    return os.path.isfile(file_path)

def parse_yaml_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError:
        print(f"Error: file ({file_name}) does not exist!") 
        return None, None, None
    
    try:
        project_name = data['project']
        repo_url = data['repo-url']
        code_files = data['code-files']
        test_suites = []
        for code_file in code_files:
            test_cases = [(test_case['name'], test_case['command'], test_case['expected-stdout']) for test_case in code_file['test-cases']]
            test_suites.append((code_file['path'], test_cases))
    except KeyError as e:
        print(f"Error: parsing yaml file, missing key:{e}")
        return None, None, None
    return project_name, repo_url, test_suites

def clone_repo(repo_link):
    print(f"Cloning {repo_link}...")
    try:
        repo_name = repo_link.split('/')[-1].split('.')[0]
        if os.path.isdir(repo_name):
            print("Already cloned!")
        else:
            process = subprocess.Popen(['git', 'clone', repo_link], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, stderr = process.communicate()
            stderr = stderr.decode('utf-8')
            if "Fatal" in stderr or "fatal" in stderr or "error" in stderr or "Error" in stderr or "ERROR" in stderr:
                raise Exception(stderr)
            print("Cloned successfully!")
    except Exception as e:
        print(f"Error: {e}")
        exit()

def get_runtime_tag(code_file_name):
    file_extension = code_file_name.split('.')[-1]
    runtime_tags = {
        'py': 'py',
        'js': 'node',
        'rb': 'rb',
        'cs': 'cs',
        'cob': 'cob',
        'ts': 'ts'
    }
    if file_extension in runtime_tags:
        return runtime_tags[file_extension]
    else:
        raise Exception("Error: file extension not supported!")

def get_metacall_process():
    try:
        process = subprocess.Popen(['metacall'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Metacall CLI started...")
        return process
    except:
        print("Error: passing options to metacall or metacall is not installed!")

def pass_options_to_metacall(process, options):
    try:
        for option in options:
            option += '\n'
            process.stdin.write(option.encode('utf-8'))
            process.stdin.flush()
        stdout, _ = process.communicate()
        out_str = stdout.decode('utf-8').strip().split('λ')
    except:
        print("Error: passing options to metacall or metacall is not installed!")
    return out_str

def run_in_cli(options):
    try:
        p = get_metacall_process()
        return pass_options_to_metacall(p, options)
    except:
        print("Error: passing options to metacall or metacall is not installed!")
        exit()

def compare_output(actual, expected_pattern):
    actual_combined = ''.join(actual).strip()
    if re.search(expected_pattern, actual_combined, re.DOTALL):
        return True
    else:
        return False

def main():
    test_suite_file_name = args.file
    project_name, repo_url, test_suites = parse_yaml_file(test_suite_file_name)
    clone_repo(repo_url)

    print(f"{project_name}\n================================")
    for test_suite in test_suites:
        file_path, test_cases = test_suite
        file_name = file_path.split('/')[-1]

        print(f"{file_name}\n=============")
        for test_case_order, test_case in enumerate(test_cases):
            test_case_name, test_case_command, test_case_expected_stdout = test_case
            commands = ['load ' + ' ' + get_runtime_tag(file_name) + ' ' + file_path]
            print(f"Test Case Command: {test_case_command}")
            commands.append(test_case_command)
            commands.append('exit')
            out_str = run_in_cli(commands)[2]
            print(f"Output String: {''.join(out_str)}")
            print(f"Expected Output: {test_case_expected_stdout}")  
            passed = compare_output(out_str, test_case_expected_stdout)
            print(f"Test Case: {test_case_name} {'PASSED' if passed else 'FAILED'}")
            print("-------------")

if __name__ == '__main__':
    main()
