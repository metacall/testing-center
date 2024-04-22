import yaml
import os
import subprocess


def Print(message, verbose=True, color='\033[0m'):
    # This is a wrapper function for the Print function
    if verbose == False:
        return
    # add the color to the message
    message = f"{color}{message}\033[0m"
    print(message)


def cloneRepo(repoLink, verbose=False):
    Print(f"Cloning {repoLink}...", color='\033[90m', verbose=verbose)
    try:
        repoName = repoLink.split('/')[-1].split('.')[0]
        # check if the repo is already cloned
        if os.path.isdir(repoName):
            Print("Already cloned!", color='\033[92m', verbose=verbose)
        else:
            # We use the `subprocess.Popen` function to start the "git" command as a child process.
            # We specify `stdin=subprocess.PIPE` to redirect its standard input stream to our Python program.
            process = subprocess.Popen(['git', 'clone', repoLink],
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            # Finally, we wait for the command to finish by calling `communicate()` on our process handle.
            _, stderr = process.communicate()
            # Check if there is an error
            stderr = stderr.decode('utf-8')
            if "Fatal" in stderr or "fatal" in stderr or "error" in stderr or "Error" in stderr or "ERROR" in stderr:
                raise Exception(stderr)
            Print("Cloned successfully!", color='\033[92m', verbose=verbose)
    except Exception as e:
        print(f"Error: {e}", verbose=verbose, color='\033[91m')
        exit()


def installDependencies(directory):
    for root, dirs, files in os.walk(directory):
        if 'package.json' in files:
            print(f"Found package.json in {root}")
            try:
                subprocess.run(["npm", "install"], cwd=root, check=True)
                print("npm install executed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"npm install failed with error: {e}")

        if 'requirements.txt' in files:
            print(f"Found requirements.txt in {root}")
            try:
                subprocess.run(["pip", "install", "-r", "requirements.txt"], cwd=root, check=True)
                print("pip install -r requirements.txt executed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"pip install -r requirements.txt failed with error: {e}")


def getRuntimeTag(fileName):
    # get the file extension
    fileExtension = fileName.split('.')[-1]
    if fileExtension == 'py':
        return 'py'
    elif fileExtension == 'js':
        Print(
            "Notice that the default runtime is node, if you want to use the V8 JavaScript Engine, please add xxxxxx",
            color='\033[90m')
        return 'node'  # or js   - V8 JavaScript Engine
    elif fileExtension == 'rb':
        return 'rb'
    elif fileExtension == 'cs':
        return 'cs'
    elif fileExtension == 'cob':
        return 'cob'
    elif fileExtension == 'ts':
        return 'ts'
    elif fileExtension == 'cob':
        return 'cob'
    else:
        return file  # Files (for handling file systems)


def checkIfFileExists(filePath):
    # check if the file exists
    if os.path.isfile(filePath):
        return True
    return False

# Parse this yaml file:
def parseYamlFile(fileName, verbose=False):
    try:
        with open(fileName, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError:
        Print(f"Error: file {fileName} does not exist!",
                    color='\033[91m',
                    verbose=verbose)
        exit()
    try:
        projectName = data['project']
        repoUrl = data['repo-url']
        codeFiles = []  # a list of test suites tuples (name, steps)
        for codeFile in data['code-files']:
            if not checkIfFileExists(filePath=codeFile['path']):
                Print(
                    f"Error: file {codeFile['path']} does not exist!",
                    color='\033[91m',
                    verbose=verbose)
                exit()
            testCases = []
            for testCase in codeFile['test-cases']:
                testCases.append((testCase['name'], testCase['command'],
                                  testCase['expected-stdout']))
            fileName = codeFile['path'].split('/')[-1]
            codeFiles.append((fileName, codeFile['path'], testCases))
    except KeyError as e:
        Print("Error: parsing yaml file!", color='\033[91m', verbose=verbose)
        Print(f"Missing key:{e}", color='\033[91m', verbose=verbose)
        exit()
    return projectName, repoUrl, codeFiles
