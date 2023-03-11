import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-V", "--verbose", action="store_true", help="increase output verbosity", default=False)
# add another argument -f that waits for a file name
parser.add_argument("-f", "--file", action="store",help="the test suite file name")
args = parser.parse_args()

    

def getSuiteFileName():
    return args.file
def getVerbose():
    return args.verbose