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
	sed 's/ip-server/$(ip)/g' ./web/index_original.html > ./web/index.html
inicio:
	@echo "Iniciando contenedores"
	sudo docker-compose -f docker-compose.yaml up -d
influx_user: 
	@echo "Creando usuario de sistema"
	adduser --system --no-create-home --disabled-login --shell /bin/bash influx_updater
	sudo usermod -aG docker influx_updater
exec: 
	@echo "Ejecución periódica del servicio"
	cp recolector_metricas.py /usr/local/bin
	sudo chown influx_updater /usr/local/bin/recolector_metricas.py
	cp influxdb_write_server.service /etc/systemd/system/
	systemctl daemon-reload
	systemctl start influxdb_write_server.service
	systemctl enable influxdb_write_server.service
stop:
	systemctl stop influxdb_write_server.service
start:
	systemctl start influxdb_write_server.service
status:
	systemctl status influxdb_write_server.service
