# This is a sample code in Python that uses the subprocess module to run the "metacall" command 
# and pass input values through its standard input stream.

import subprocess
import re

def getOptions(fileName):
    # read the options from the file
    with open(fileName, 'r') as f:
        options = f.readlines()
    return options

def getMetacallProcess():
    # We use the `subprocess.Popen` function to start the "metacall" command as a child process. 
    # We specify `stdin=subprocess.PIPE` to redirect its standard input stream to our Python program. 
    p = subprocess.Popen(['metacall'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Run the "metacall" command and get a handle to its standard input stream
    return p

def passOptionsToMetacall(p, options):
    # We send some input values to the standard input stream using the `write` method of the `stdin` object. 
    # Note that we need to encode the string as bytes before sending it.
    for option in options:
        p.stdin.write(option.encode('utf-8'))
    # Finally, we wait for the command to finish by calling `communicate()` on our process handle.
    # This returns a tuple of two byte strings: one for stdout and one for stderr.
    stdout, stderr = p.communicate()
    # We then decode it into a string using `decode()` and print it out.
    outStr = stdout.decode('utf-8')
    errStr = stderr.decode('utf-8')
    return outStr, errStr

def getOutputList(outStr): 
    # Split the output string into a list of strings by the λ character
    outputList = outStr.split('λ')
    return outputList  

def checkOutput(output, expectedOutput, expectedRegex):
    # check if the output is the same as the expected output
    if expectedOutput is not None:
        if output == expectedOutput:
            print('Test passed!')
        else:
            print('Test failed!')
    # check if the output matches the expected regex
    else:
        if re.match(expectedRegex, output):
            print('Test passed!')
        else:
            print('Test failed!')

def main():
    options = getOptions('commands/metacallcli-node-null-undefined.txt')
    p = getMetacallProcess()
    outStr, errStr = passOptionsToMetacall(p, options)
    outputList = getOutputList(outStr)
    checkOutput(outputList[3], None, ".*Error.*undefined.*")
    with open('output.txt', 'w') as f: # print the output in output.txt
        f.truncate(0) # clean the file
        f.write(outStr) # write the output


if __name__ == '__main__':
    main()



