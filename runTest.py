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
    process = subprocess.Popen(['metacall'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Run the "metacall" command and get a handle to its standard input stream
    return process

def passOptionToMetacall(process, options, saveOutput=False):
    # We send some input values to the standard input stream using the `write` method of the `stdin` object. 
    # Note that we need to encode the string as bytes before sending it.
    for option in options:
        process.stdin.write(option.encode('utf-8'))
    # Finally, we wait for the command to finish by calling `communicate()` on our process handle.
    # This returns a tuple of two byte strings: one for stdout and one for stderr.
    stdout, stderr = process.communicate()
    # We then decode it into a string using `decode()` and print it out.
    outStr = stdout.decode('utf-8')
    errStr = stderr.decode('utf-8')
    if saveOutput:
        with open('output.txt', 'w') as f: # print the output in output.txt
            f.truncate(0) # clean the file
            f.write(outStr) # write the output
    return outStr, errStr

def getOutputList(outStr, separator='λ'): 
    # Split the output string into a list of strings by the λ character
    outputList = outStr.split(separator)
    return outputList  

def checkOutput(output, expectedOutput):
    print(re.search(expectedOutput, output))
    if re.search(expectedOutput, output):
        print('Test passed!')
    else:
        print('Test failed!')

def main():
    options = getOptions('test-suits/random-password-generator-example.txt')
    metacallProcess = getMetacallProcess()
    outStr, _ = passOptionToMetacall(process=metacallProcess, options=options, saveOutput=True)
    outputList = getOutputList(outStr=outStr)
    print(outputList[3])
    checkOutput(output=outputList[3], expectedOutput="\s+[a-zA-Z0-9!-\/]{12}")
    


if __name__ == '__main__':
    main()




