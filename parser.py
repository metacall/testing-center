import subprocess
import re
import yaml
import select


def getMetacallProcess():
    # We use the `subprocess.Popen` function to start the "metacall" command as a child process. 
    # We specify `stdin=subprocess.PIPE` to redirect its standard input stream to our Python program. 
    process = subprocess.Popen(['metacall'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Run the "metacall" command and get a handle to its standard input stream
    return process
def passOptionsToMetacall(process, options):
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
   
    return outStr[-2], errStr

def cloneRepo(repoLink):
    # CLone the repo using git
    try:
        subprocess.call([
            'git', 'clone',  + repoLink
        ])
        return True
    except:
        return False
# Parse this yaml file:

def parseYamlFile(fileName):
    with open(fileName, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    projectName = data['project']
    repoUrl = data['repo-url']
    codeFiles = [] # a list of test suites tuples (name, steps)
    for codeFile in data['code-files']:
        testCases = []
        for testCase in codeFile['test-cases']:
            testCases.append((testCase['name'], testCase['command'], testCase['expected-stdout'], testCase['expected-stderr'], testCase['expected-exit-code']))
            codeFiles.append((codeFile['name'], codeFile['runtime-tag'], codeFile['path'],testCases))
    return projectName, repoUrl, codeFiles
            

def compareStrings(targetString, expectedString):
    # print(re.search(expectedOutput, output))
    if re.search(expectedString, targetString):
        return True
    else:
        return False


        
def main():
    projectName, repoUrl, codeFiles = parseYamlFile('test-suits/test-random-password-generator-example.yaml')
    print("================================")
    print("Testing:", projectName)
    print("Cloning:", repoUrl)
    if cloneRepo(repoUrl):
        print("Cloned successfully!")
    else:
        print("Already cloned!")
    print("Running tests for:", projectName)
    print("================================")
    for codeFile in codeFiles:
        print("Testing:", codeFile[0])
        print("=============")
        for testCase in codeFile[3]:
            metacallProcess = getMetacallProcess()
            commands = ['load ' + codeFile[1] + ' ' + codeFile[2]]
            print("Test case:", testCase[0])
            print("Command: ", testCase[1])
            commands.append(testCase[1])
            outStr, errStr = passOptionsToMetacall(process=metacallProcess, options=commands)
            print("Expected stdout: ", testCase[2])
            print("stdout: ", outStr)
            c1 = compareStrings(targetString=outStr, expectedString=testCase[2])
            print("Expected stderr: ", testCase[3])
            print("stderr: ", errStr)
            c2 = compareStrings(targetString=errStr, expectedString=testCase[3])
            print("Expected exit code: ", testCase[4])
            exitCode = metacallProcess.returncode
            print("Exit code: ", exitCode)
            c3 = exitCode == testCase[4]
            if c1 and c2 and c3:
                print("Test passed!")
            else:
                print("Test failed!")
            print("-------------")


if __name__ == '__main__':
    main()
