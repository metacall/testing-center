# MetaCall Project Notes
The idea is to write a Js or py script that:
1. Downloads and installs metacall.
2. Clones each example repo.
3. Loads it with metacall cli.
4. Verifies that works.
5. Deploys it with metacall deploy cli.


Helpful commands:
1. Install Docker: `wget -O - https://gist.githubusercontent.com/fredhsu/f3d927d765727181767b3b13a3a23704/raw/3c2c55f185e23268f7fce399539cb6f1f3c45146/ubuntudocker.sh | bash`
2. Copy a file though ssh to the server: `sudo scp -i ./terraform/keys/gp.pem ./test.py user<>@<server IP>:~/`
3. To build the image: `docker build -t python-app .`.
4. To run and enter the container: `docker run -it python-app /bin/bash`.
5. Run the container and mount the current directory to the container: `docker run -it -v $(pwd):/app python-app /bin/bash` or `docker run -it -v .:/app python-app /bin/bash`
6. To list docker containers:` docker ps -a`.
7. To delete all containers: `docker container prune`.
8. Run the script: `python3 main.py`.

sudo scp -i ./gp.pem ./main.py ubuntu@ec2-54-174-110-124.compute-1.amazonaws.com:~/
sudo scp -i ./gp.pem ./Dockerfile ubuntu@ec2-54-174-110-124.compute-1.amazonaws.com:~/

