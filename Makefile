python:
	@echo "Instalando Python"
	apt update
	apt install python3.8
librerias: requirements.txt
	@echo "Instalando liberías"
	pip install -r requirements.txt
influxDB:
	@echo "Instalando InfluxDB"
	curl -sL https://repos.influxdata.com/influxdb.key | apt-key add -
	apt update
	apt install influxdb
inicio:
	@echo "Iniciando contenedores"
	docker-compose -f docker-compose.yaml up
cron:
	@echo "Ejecucion periodica"
	crontab -l > micron
	echo "* * * * * sleep 00; timeout 15s python recolector.py" >> micron
	echo "* * * * * sleep 15; timeout 15s python recolector.py" >> micro
	echo "* * * * * sleep 30; timeout 15s python recolector.py" >> micro
	echo "* * * * * sleep 45; timeout 15s python recolector.py" >> micro
	crontab micron
	rm micron
