import subprocess
import re
import yaml
import sys


def Print(string, verbose=True):
    if not verbose:
        return
    # This is a wrapper function for the Print function
    print(string)


def cloneRepo(repoLink):
    try:
        # We use the `subprocess.Popen` function to start the "git" command as a child process.
        # We specify `stdin=subprocess.PIPE` to redirect its standard input stream to our Python program.
        # check if the repo is already cloned
        process = subprocess.Popen(['ls'],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        outStr, _ = process.communicate()
        outStr = outStr.decode('utf-8').strip()
        if repoLink.split('/')[-1].split('.')[0] in outStr:
            return False
        else:
            process = subprocess.Popen(['git', 'clone', repoLink],
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            # Finally, we wait for the command to finish by calling `communicate()` on our process handle.
            process.communicate()
    except:
        return False


def getRuntimeTag(fileName):
    # get the file extension
    fileExtension = fileName.split('.')[-1]
    if fileExtension == 'py':
        return 'py'
    elif fileExtension == 'js':
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


# Parse this yaml file:
def parseYamlFile(fileName):
    try:
        with open(fileName, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError:
        Print("File not found!")
        exit()
    try:
        projectName = data['project']
        repoUrl = data['repo-url']
        codeFiles = []  # a list of test suites tuples (name, steps)
        for codeFile in data['code-files']:
            testCases = []
            for testCase in codeFile['test-cases']:
                testCases.append((testCase['name'], testCase['command'],
                                  testCase['expected-stdout']))
            codeFiles.append((codeFile['name'], codeFile['path'], testCases))
    except KeyError as e:
        Print("Error: parsing yaml file!")
        Print("Missing key:", e)
        exit()
    return projectName, repoUrl, codeFiles


def compareStrings(targetString, expectedString, verbose=False):
    try:
        if verbose:
            Print(f"Expected stdout: {expectedString}")
        matchObj = re.search(expectedString, targetString)
        if matchObj:
            if verbose:
                out = re.sub(expectedString,
                             "\033[92m" + matchObj.group() + "\033[0m",
                             targetString)
                Print(f"stdout: {out}")
            return True
        else:
            Print(f"stdout: {targetString}")
            return False
    except TypeError:
        Print("Error: expected stdout is not a string!")
        return False


def printTestResults(codeFile, successCount, failedTestCases):
    try:
        if successCount == len(codeFile[2]):
            Print(
                f"\033[92m{successCount}/{len(codeFile[2])} test case{'s' if successCount > 1 else ''} passed for: {codeFile[0]} \033[0m"
            )
        else:
            Print(
                f"\033[91m{len(codeFile[2]) - successCount}/{len(codeFile[2])} test case{'s' if len(codeFile[2]) - successCount > 1 else ''} failed for: {codeFile[0]} \033[0m"
            )
            Print("Failed test cases:")
            for failedTestCase in failedTestCases:
                Print(
                    f"\033[91m{failedTestCase[0] + 1}. {failedTestCase[1]}\033[0m"
                )
    except:
        return


def getSuiteFileName():
    return sys.argv[1]