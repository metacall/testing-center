# MetaCall Project Notes

## Objective
The idea is to write a Js or py script that:
1. Downloads and installs metacall.
2. Clones each example repo.
3. Loads it with metacall cli.
4. Verifies that works.
5. Deploys it with metacall deploy cli.


## Helpful commands
1. Install Docker: `wget -O - https://gist.githubusercontent.com/fredhsu/f3d927d765727181767b3b13a3a23704/raw/3c2c55f185e23268f7fce399539cb6f1f3c45146/ubuntudocker.sh | bash`
2. Copy a file though ssh to the server: `sudo scp -i ./terraform/keys/gp.pem ./test.py user<>@<server IP>:~/`
3. To build the image: `docker build -t python-app .`.
4. To run and enter the container: `docker run -it python-app /bin/bash`.
5. Run the container and mount the current directory to the container: `docker run -it -v $(pwd):/app python-app /bin/bash` or `docker run -it -v .:/app python-app /bin/bash`
6. To list docker containers:` docker ps -a`.
7. To delete all containers: `docker container prune`.
8. Run the script: `python3 main.py`.

## Important Notes
1. We will install the cli anyway we don't need to check if it's installed.
2. This is a [test example](https://github.com/metacall/core/blob/develop/source/cli/metacallcli/test/commands/metacallcli-tsx-templating.txt). The code is **loading a template file** written in TypeScript, named "templating.tsx". It then **inspects the code to check for any errors or warnings**. Then it **calls a function named "hello" with the argument "metaprogrammer"**. Finally, **the code exits** the program. 
3. We run metacall as **repl** and we **pipe** this to **stdin** then we **get the output** and **check for the result**, or **regex the stdout**.
4. Create a function that you can pass something like [this](https://github.com/metacall/core/blob/develop/source/cli/metacallcli/test/commands/metacallcli-tsx-templating.txt) and you can get the stdout. Something like that is in the deploy/cli. [1](https://github.com/metacall/deploy/blob/8b25ac18d92939cc62930b0e412798f2aa737a3b/src/test/cli.integration.spec.ts#L87) and [2](https://github.com/metacall/deploy/blob/8b25ac18d92939cc62930b0e412798f2aa737a3b/src/test/cli.integration.spec.ts#L166)
5. some tests will also need metacall a.js so we need both versions.
6. Run something like 
    - ``` bash 
        git clone https://github.com/metacall/examples
        cd examples
        metacall
        load node examples/auth-middleware/middleware.js
        call signin("viferga", 123)
        exit
        ```
    - now, with this you grep the stdout you should check if signin returns correctly

## Helpful links
- [subprocess and streams](https://realpython.com/python-subprocess/#the-standard-io-streams)


## Currently Available Commands in the cli
- `help`: Show help for MetaCall CLI (Use this command to see the usage of a particular command)
- `load`: Load a script from file into MetaCall
- `inspect`: Show all runtimes, modules and functions (with their signature) loaded into MetaCall
- `call`: Call a function previously loaded in MetaCall (Note: For js and py functions that do not return anything, the default return value is a null)
- `await`: Await an async function previously loaded in MetaCall
- `clear`: Delete a script previously loaded in MetaCall
- `exit`: Exit from MetaCall CLI