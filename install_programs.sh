#!/bin/bash

sudo apt-get update --yes

python=$(dpkg -s python3 | grep installed)

if [ "$python" = "" ]; then
	sudo apt-get --yes install python3
else
	echo "Python ya esta instalado"
fi

python3_pip=$(dpkg -s python3-pip | grep installed)

if [ "$python3_pip" = "" ]; then
	sudo apt --yes install python3-pip
else
	echo "Python3-pip ya esta instalado"
fi

docker=$(which docker)

if [ "$docker" = "" ]; then
	sudo apt-get --yes install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
	echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

else
	echo "Docker ya esta instalado"
fi

docker_compose=$(which docker-compose)
if [ "$docker_compose" = "" ]; then
	sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose
else
	echo "Docker-compose ya esta instalado"
fi




