#!/usr/bin/env python3
from influxdb import InfluxDBClient
from datetime import datetime

def leer_comentarios(client):
    # Leer los comentarios existentes

    result = client.query("SELECT * from metricas") # Query de todos los datos de todos los comentarios
    comentarios = []    # Array que almacenará todos los comentarios leídos para guardarlos posteriormente
    print("{:17}{:13}{:13}{:13}{:13}{:13}{:13}{:13}{:13}{}".format("Nombre","CPU","Mem. Usada","Mem. Limite","Memoria %", "Net imput", "Net Out", "Block In.", "Block Out.", "PIDs")) # Título. Para que quede elegante
    for t in result:
      for i in t:
        # Loop por todos los comentarios leídos en nuestra query
        print("{:14} | {:10} | {:10} | {:10} | {:10} | {:10} | {:10} | {:10} | {:10} | {}".format(i['nombre'],i['cpu'],i['mem_usada'],i['mem_limite'],i['mem_porcentaje'],i['net_input'],i['net_output'],i['block_input'],i['block_output'],i['pids']))


def main_loop():
    # Loop principal del programa

    # Creamos el cliente InfluxDB con la librería InfluxDBClient, aportándole los datos necesarios.
    client = InfluxDBClient(host = 'localhost', port = 8086, username = 'admin', password = 'admin', database = 'influx_db')
    client.switch_database('influx_db') # equivalente a "USE influx_db"
    leer_comentarios(client)


if __name__ == "__main__":
    main_loop()
