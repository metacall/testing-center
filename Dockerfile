# Specifying the base image
FROM python:3.10

# Act as a root user
USER root

# Set the working directory
WORKDIR /app


# To build the image: docker build -t python-app .
# To run and enter the container: docker run -it python-app /bin/bash
# Run the container and mount the current directory to the container: docker run -it -v $(pwd):/app python-app /bin/bash
# To list docker containers: docker ps -a
# To delete all containers: docker container prune