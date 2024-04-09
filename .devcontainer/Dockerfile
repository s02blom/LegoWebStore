#FROM mcr.microsoft.com/vscode/devcontainers/php:8-bullseye
FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# update apt
RUN apt update

# install httpie
RUN apt-get install -y python3-pip 
RUN apt-get install -y libmariadb-dev 

WORKDIR ~
ENTRYPOINT ["/bin/bash"]
