# Objective:
# The idea is to write a Js or py script that:
# 1. Downloads and installs metacall.
# 2. Clones each example repo.
# 3. Loads it with metacall cli.
# 4. Verifies that works.
# 5. Deploys it with metacall deploy cli.

import os
import sys
import subprocess

############################################################################################################
# 0. Gets the operating system.
def getOperatingSystem():
    if sys.platform == 'win32':
        return 'windows'
    elif sys.platform == 'darwin':
        return 'mac'
    elif sys.platform == 'linux':
        return 'linux'


# 1. Downloads and installs metacall.
def downloadAndInstallMetacall(operatingSystem):
    # Download and install metacall.
    try:
        if operatingSystem == 'linux' or operatingSystem == 'mac':
            subprocess.call([
                'wget', '-O', 'install.sh',
                'https://raw.githubusercontent.com/metacall/install/master/install.sh'
            ])
            subprocess.call(['chmod', '+x', 'install.sh'])
            subprocess.call(['./install.sh'])
        # elif operatingSystem == 'windows':
        #     subprocess.call(['powershell', '-NoProfile', '-ExecutionPolicy', 'unrestricted', '-Command', '“[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; &([scriptblock]::Create((Invoke-WebRequest -UseBasicParsing ‘https://raw.githubusercontent.com/metacall/install/master/install.ps1')))"'])
        return True
    except:
        return False



# 2. Clones an example repo.
def cloneExampleRepo(repoName):
    # Check if the repo is already cloned.
    if os.path.isdir(repoName):
        print('Repo already cloned.')
        return
    # Create a new directory for the repo and download it into it.
    # subprocess.call(['wget', '--no-check-certificate', 'https://github.com/metacall/' + repoName + '/tarball/master', '-O', repoName + '.tar.gz'])
    # subprocess.call(['tar', '-xf', '--strip-components=1', '-C', repoName, repoName + '.tar.gz'])
    # CLone the repo using git
    try:
        subprocess.call([
            'git', 'clone', 'https://github.com/metacall/' + repoName + '.git'
        ])
        return True
    except:
        return False


# 3. Run the example repo.
def runExampleRepo(repoName):
    entryPoint = 'main.js'
    # Check if the run command ran successfully.
    try:
        subprocess.call(['cd ', repoName])
        subprocess.call(['metacall ', './' + entryPoint])
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    # 0. Gets the operating system.
    operatingSystem = getOperatingSystem()
    print('Operating system: ' + operatingSystem)
    # 1. Downloads and installs metacall.
    if not downloadAndInstallMetacall(operatingSystem):
        print('Error: Could not install metacall.')
        sys.exit(1)
    print('Metacall installed successfully.')
    # 2. Clones an example repo.
    repoName = 'examples'
    cloneExampleRepo(repoName)
    print('Example repo cloned successfully.')
    # 3. Run the example repo.
    if not runExampleRepo(repoName):
        print('Error: Could not run example repo.')
        sys.exit(1)
    print('Example repo ran successfully.')
