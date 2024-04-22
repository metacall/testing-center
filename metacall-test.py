#!/usr/bin/python3

import sys
from utilities import parseYamlFile, getRuntimeTag, cloneRepo, Print, installDependencies
from utilitiesCli import runInCLI
from utilitiesResults import compareStrings, printTestResults
from utilitiesArgParser import getSuiteFileName, getVerbose


def main():
    # accept the test suite file name as an argument
    testSuiteFileName = getSuiteFileName()
    verbose = getVerbose()
    projectName, repoUrl, codeFiles = parseYamlFile(testSuiteFileName, verbose=verbose)
    Print(f"{projectName}", color='\033[94m', verbose=verbose)
    cloneRepo(repoUrl, verbose=verbose)
    # installDependencies("examples")

    Print("================================", verbose=verbose)
    for codeFile in codeFiles:
        Print(f"Testing: {codeFile[0]}\n=============", verbose=verbose)
        successCount = 0
        failedTestCases = []
        for testCaseOrder, testCase in enumerate(codeFile[2]):
            commands = [
                'load' + ' ' + getRuntimeTag(codeFile[0]) + ' ' + codeFile[1]
            ]
            Print(f"- {testCase[0]}", color='\033[94m', verbose=verbose)
            Print(f"Command: {testCase[1]}", verbose=verbose)
            commands.extend([testCase[1], "exit"])
            outStr = runInCLI(options=commands)
            # print(commands)
            # print(outStr)
            if compareStrings(targetString=outStr,
                              expectedString=testCase[2],
                              verbose=verbose):
                successCount += 1
                Print(f"test case {testCaseOrder+1} passed for: {codeFile[0]}\n-------------",
                      color='\033[92m',
                      verbose=verbose)
            else:
                failedTestCases.append((testCaseOrder, testCase[0]))
                Print(f"test case {testCaseOrder+1} failed for: {codeFile[0]}\n-------------",
                      color='\033[91m',
                      verbose=verbose)
        printTestResults(codeFile=codeFile,
                         successCount=successCount,
                         failedTestCases=failedTestCases,
                         verbose=verbose)


if __name__ == '__main__':
    main()