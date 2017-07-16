FROM ubuntu:latest

MAINTAINER Radu Suciu <radusuciu@gmail.com>

# Create user with non-root privileges
RUN adduser --disabled-password --gecos '' dance
RUN chown -R dance /home/dance

# install some deps
RUN apt-get update && apt-get -y install python3-pip python3-venv

WORKDIR /home/dance/savesoundcloud
USER dance
CMD [ "/bin/bash", "/home/dance/savesoundcloud/start.sh" ]
