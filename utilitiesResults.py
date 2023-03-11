import re
from utilities import Print


def compareStrings(targetString, expectedString, verbose=False):
    try:
        Print(f"Expected stdout: {expectedString}", verbose=verbose)
        matchObj = re.search(expectedString, targetString)
        if matchObj:
            if verbose:
                out = re.sub(expectedString,
                             "\033[92m" + matchObj.group() + "\033[0m",
                             targetString)
                Print(f"stdout: {out}", verbose=verbose)
            return True
        else:
            Print(f"stdout: {targetString}")
            return False
    except TypeError:
        Print("Error: expected stdout is not a string!",
              color='\033[91m',
              verbose=verbose)
        return False


def printTestResults(successCount, codeFile, failedTestCases, verbose=False):
    # This function will always print the results of the test cases
    try:
        # The message is "Summary" in a box
        Print("=================\n=====SUMMARY=====\n=================")
        numTestCases = codeFile[2]
        if successCount == len(numTestCases):
            Print(
                f"{successCount}/{len(numTestCases)} test case{'s' if successCount > 1 else ''} passed for: {codeFile[0]}",
                color='\033[92m')
        else:
            Print(
                f"{len(numTestCases) - successCount}/{len(numTestCases)} test case{'s' if len(numTestCases) - successCount > 1 else ''} failed for: {codeFile[0]}:",
                color='\033[91m')
            for failedTestCase in failedTestCases:
                Print(f"- Test Case {failedTestCase[0] + 1}: {failedTestCase[1]}",
                      color='\033[91m')
    except:
        return

