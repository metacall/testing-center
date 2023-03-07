# This is a sample code in Python that uses the subprocess module to run the "metacall" command 
# and pass input values through its standard input stream.

import subprocess


# We then send some input values (in this case, just a string) to the standard input stream using the `write` method of the `stdin` object. 
# Note that we need to encode the string as bytes before sending it.

# Finally, we wait for the command to finish by calling `communicate()` on our process handle. 
# This returns a tuple of two byte strings: one for stdout and one for stderr. 
# We only care about stdout in this case, so we assign it to `output_bytes`. 
# We then decode it into a string using `decode()` and print it out.

def getMetacallProcess():
    # We use the `subprocess.Popen` function to start the "metacall" command as a child process. 
    # We specify `stdin=subprocess.PIPE` to redirect its standard input stream to our Python program. 
    p = subprocess.Popen(['metacall'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Run the "metacall" command and get a handle to its standard input stream
    return p

def passOptionToMetacall(p, option):
    # Send input values to the standard input stream
    inputStr = f"{option}\n"

    stdout, stderr = p.communicate(inputStr.encode('utf-8'))
    # convert the output to a string
    outStr = stdout.decode('utf-8')
    errStr = stderr.decode('utf-8')
    # print the type of outputBytes
    print(outStr)
    # print the output in output file called output.txt
    with open('output.txt', 'w') as f:
        f.write(outStr)
    # p.stdin.write(input_str.encode('utf-8'))

def main():
    p = getMetacallProcess()
    passOptionToMetacall(p, 'help')


main()





# input_str = 'help'
# getOption = subprocess.run(["echo", input_str], stdout=subprocess.PIPE)
# metacallProcess = subprocess.run(
#     ["metacall"], input=getOption.stdout, stdout=subprocess.PIPE
# )
# print(metacallProcess.stdout.decode("utf-8"))
