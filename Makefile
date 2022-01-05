ip =$(shell curl whatismyip.akamai.com -w "\n")
all: programas librerias set_ip inicio influx_user exec
inicializar: set_ip inicio
programas:
	@echo "Instalando Programas necesarios"
	sudo chmod +x install_programs.sh
	./install_programs.sh
librerias:
	@echo "Instalando liberías"
	pip3 install influxdb
set_ip:
	@echo "Estableciendo ip del servidor actual..." 
	sudo sed 's/ip-server/$(ip)/g' ./web/index_original.html > ./web/index.html
inicio:
	@echo "Iniciando contenedores"
	sudo docker-compose -f docker-compose.yaml up -d
influx_user: 
	@echo "Creando usuario de sistema"
	sudo adduser --system --no-create-home --disabled-login --shell /bin/bash influx_updater
	sudo usermod -aG docker influx_updater
exec: 
	@echo "Ejecución periódica del servicio"
	sudo cp recolector_metricas.py /usr/local/bin
	sudo chown influx_updater /usr/local/bin/recolector_metricas.py
	sudo cp influxdb_write_server.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl start influxdb_write_server.service
	sudo systemctl enable influxdb_write_server.service
stop:
	sudo systemctl stop influxdb_write_server.service
start:
	sudo systemctl start influxdb_write_server.service
status:
	sudo systemctl status influxdb_write_server.service
