import subprocess
import re
import yaml
import sys


def getMetacallProcess():
    try:
        # We use the `subprocess.Popen` function to start the "metacall" command as a child process. 
        # We specify `stdin=subprocess.PIPE` to redirect its standard input stream to our Python program. 
        process = subprocess.Popen(['metacall'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Run the "metacall" command and get a handle to its standard input stream
        return process
    except:
        return None
def passOptionsToMetacall(process, options):
    try:
        # We send some input values to the standard input stream using the `write` method of the `stdin` object. 
        # Note that we need to encode the string as bytes before sending it.
        for option in options:
            option += '\n' # add a new line character to the end of the option
            process.stdin.write(option.encode('utf-8'))
            process.stdin.flush()
        # Finally, we wait for the command to finish by calling `communicate()` on our process handle.
        # This returns a tuple of two byte strings: one for stdout and one for stderr.
        stdout, stderr = process.communicate()
        # We then decode it into a string using `decode()` and print it out.
        outStr = stdout.decode('utf-8').strip().split('λ') # split the output by the λ character
        errStr = stderr.decode('utf-8')
    except:
        print("Error: passing options to metacall or metacall is not installed!")
        return None, None
    return outStr[-2], errStr

def cloneRepo(repoLink):
    try:
        # We use the `subprocess.Popen` function to start the "git" command as a child process.
        # We specify `stdin=subprocess.PIPE` to redirect its standard input stream to our Python program.
        # check if the repo is already cloned
        process = subprocess.Popen(['ls'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outStr, _ = process.communicate()
        outStr = outStr.decode('utf-8').strip()
        if repoLink.split('/')[-1].split('.')[0] in outStr:
            return False
        else:
            process = subprocess.Popen(['git', 'clone', repoLink], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Finally, we wait for the command to finish by calling `communicate()` on our process handle.
            process.communicate()
    except:
        return False


# Parse this yaml file:
def parseYamlFile(fileName):
    try:
        with open(fileName, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError:
        print("File not found!")
        exit()
    try:
        projectName = data['project']
        repoUrl = data['repo-url']
        codeFiles = [] # a list of test suites tuples (name, steps)
        for codeFile in data['code-files']:
            testCases = []
            for testCase in codeFile['test-cases']:
                testCases.append((testCase['name'], testCase['command'], testCase['expected-stdout']))
            codeFiles.append((codeFile['name'], codeFile['runtime-tag'], codeFile['path'],testCases))
    except KeyError as e:
        print("Error: parsing yaml file!")
        print("Missing key:", e)
        exit()
    return projectName, repoUrl, codeFiles
            

def compareStrings(targetString, expectedString, verbose=False):
    try:
        if verbose:
            print("Expected stdout: ", expectedString)
            print("stdout: ", targetString)
        matchObj = re.search(expectedString, targetString)
        if matchObj:
            if verbose:
                print(re.sub(expectedString, "\033[92m" + matchObj.group() + "\033[0m", targetString))
            return True
        else:
            return False
    except TypeError:
        print("Error: expected stdout is not a string!")
        return False

def printTestResults(codeFile, successCount, failedTestCases): 
    try:    
        if successCount == len(codeFile[3]):
            # print("\033[92m" + "All test cases passed for:", codeFile[0] + "\033[0m")
            message = f"\033[92m{successCount}/{len(codeFile[3])} test case{'s' if successCount > 1 else ''} passed for: {codeFile[0]} \033[0m"
            print(message)
        else:
            message = f"\033[91m{len(codeFile[3]) - successCount}/{len(codeFile[3])} test case{'s' if len(codeFile[3]) - successCount > 1 else ''} failed for: {codeFile[0]} \033[0m"
            print(message)  
            print("Failed test cases:")
            for failedTestCase in failedTestCases:
                print(f"\033[91m{failedTestCase[0] + 1}. {failedTestCase[1]}\033[0m") 
    except:
        return 
def main():
    # accept the test suite file name as an argument
    testSuiteFileName = sys.argv[1]
    projectName, repoUrl, codeFiles = parseYamlFile(testSuiteFileName)
    print("Testing:", projectName)
    print("Cloning:", repoUrl)
    if cloneRepo(repoUrl):
        print("Cloned successfully!")
    else:
        print("Already cloned!")
    print("Running tests...")
    print("================================")
    for codeFile in codeFiles:
        print("Testing:", codeFile[0])
        print("=============")
        successCount = 0
        failedTestCases = []
        for testCaseOrder, testCase in enumerate(codeFile[3]):
            metacallProcess = getMetacallProcess()
            commands = ['load ' + codeFile[1] + ' ' + codeFile[2]]
            print("Test case:", testCase[0])
            print("Command: ", testCase[1])
            commands.append(testCase[1])
            outStr, _ = passOptionsToMetacall(process=metacallProcess, options=commands)
            if compareStrings(targetString=outStr, expectedString=testCase[2], verbose=True):
                successCount += 1
                print("\033[92m" + "Test case " + str(testCaseOrder + 1) + " passed!" + "\033[0m")
            else:
                failedTestCases.append((testCaseOrder, testCase[0]))
                print("\033[91m" + "Test case " + str(testCaseOrder + 1) + " failed!" + "\033[0m")
            print("-------------")
        printTestResults(codeFile, successCount, failedTestCases)
        

# to insert variable inside a string: f"hello {variable}"
if __name__ == '__main__':
    main()