import sys
from utilities import parseYamlFile, getRuntimeTag, compareStrings, cloneRepo, printTestResults, getSuiteFileName, Print
from utilitiesCli import runInCLI

def main():
    # accept the test suite file name as an argument
    testSuiteFileName = getSuiteFileName()
    projectName, repoUrl, codeFiles = parseYamlFile(testSuiteFileName)
    Print(
        f"\033[94mTesting:{projectName}\033[0m \n\033[94mCloning from: {repoUrl}\033[0m"
    )
    if cloneRepo(repoUrl):
        Print("Cloned successfully!")
    else:
        Print("Already cloned!")
    Print("Running tests...")
    Print("================================")
    for codeFile in codeFiles:
        Print("Testing:", codeFile[0])
        Print("=============")
        successCount = 0
        failedTestCases = []
        for testCaseOrder, testCase in enumerate(codeFile[2]):
            commands = [
                'load ' + ' ' + getRuntimeTag(codeFile[0]) + ' ' + codeFile[1]
            ]
            Print("Test case:", testCase[0])
            Print("Command: ", testCase[1])
            commands.append(testCase[1])
            outStr = runInCLI(options=commands)
            if compareStrings(targetString=outStr,
                              expectedString=testCase[2],
                              verbose=True):
                successCount += 1
                Print(
                    f"\033[92m{successCount}/{len(codeFile[2])} test case{'s' if successCount > 1 else ''} passed for: {codeFile[0]} \033[0m"
                )
            else:
                failedTestCases.append((testCaseOrder, testCase[0]))
                Print(
                    f"\033[91m{len(codeFile[2]) - successCount}/{len(codeFile[2])} test case{'s' if len(codeFile[2]) - successCount > 1 else ''} failed for: {codeFile[0]} \033[0m"
                )
            Print("-------------")
        printTestResults(codeFile, successCount, failedTestCases)


# to insert variable inside a string: f"hello {variable}"
if __name__ == '__main__':
    main()