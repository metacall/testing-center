import subprocess
import os


def getMetacallProcess():
    try:
        # We use the `subprocess.Popen` function to start the "metacall" command as a child process.
        # We specify `stdin=subprocess.PIPE` to redirect its standard input stream to our Python program.
        process = subprocess.Popen(
            ['metacall'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )  # Run the "metacall" command and get a handle to its standard input stream
        return process
    except:
        Print(
            "Error: passing options to metacall or metacall is not installed!", color='\033[91m')
        exit()


def passOptionsToMetacall(process, options):
    try:
        # We send some input values to the standard input stream using the `write` method of the `stdin` object.
        # Note that we need to encode the string as bytes before sending it.
        for option in options:
            option += '\n'  # add a new line character to the end of the option
            process.stdin.write(option.encode('utf-8'))
            process.stdin.flush()
        # Finally, we wait for the command to finish by calling `communicate()` on our process handle.
        # This returns a tuple of two byte strings: one for stdout and one for stderr.
        stdout, _ = process.communicate()  
        # the stderr is not used as metacall does not return any errors
        # We then decode it into a string using `decode()` and Print it out.
        outStr = [s.replace("\n", "") for s in stdout.decode('utf-8').split('λ ')] # split the output by the λ character
        # print(f"outstr: {outStr}")
    except:
        Print(
            "Error: passing options to metacall or metacall is not installed!", color='\033[91m')
        exit()
    return outStr[2]


def runInCLI(options):
    # This function runs the metacall CLI and passes the options to it
    try:
        p = getMetacallProcess()
        return passOptionsToMetacall(p, options)
    except:
        Print(
            "Error: passing options to metacall or metacall is not installed!", color='\033[91m')
        exit()
