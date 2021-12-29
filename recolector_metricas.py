#!/usr/bin/env python3
from influxdb import InfluxDBClient
from datetime import datetime
import subprocess
import re
def recolectar():
    datos=subprocess.Popen(["docker","stats","--no-stream"],stdout=subprocess.PIPE)
    output,err=datos.communicate()

    metricas = output.decode("utf-8").split("\n")
    #metricas = output_splitted[1].split("  ")
    lista_dic = []
    i = 1

    while i < len(metricas)-1:
        datos_splitteados = metricas[i].split(' ')
        datos_limpios = limpiar_array(datos_splitteados)
        dic = {
            "nombre": datos_limpios[0],
            "cpu": float(datos_limpios[1]),
            "mem_usada": float(datos_limpios[2]),
            "mem_limite": float(datos_limpios[3]),
            "mem_porcentaje": float(datos_limpios[4]),
            "net_input": float(datos_limpios[5]),
            "net_output": float(datos_limpios[6]),
            "block_input": float(datos_limpios[7]),
            "block_output": float(datos_limpios[8]),
            "pids": int(datos_limpios[9])
        }
        lista_dic.append(dic)
        i+=1

    return lista_dic

def limpiar_array(array):
    array_limpio = []
    i = 0
    while i <= len(array)-1:
        if array[i] != '':
            if i != 3:
                array_limpio.append(re.findall(r'-?\d+\.?\d*',array[i]))
            else:
                array_limpio.append(array[i])
        i+=1
    array_limpio2 = []
    i = 2
    array_limpio2.append(array_limpio[1])
    while i <= len(array_limpio)-1:
        if array_limpio[i]:
            array_limpio2.append(array_limpio[i][0])
        i+=1
    return array_limpio2

def subir_metricas(client, metricas):
    # Crear y escribir en la base de datos una nueva entrada
    data = [] # Lista con todas las entradas que se vayan a subir a la BBDD
    for entrada in metricas:
      datos_actuales = {
          "measurement": "metricas",      # - Algo similar a la "tabla" en la que almacenamos nuestros comentarios
          "time": datetime.now(),         # - Campo que guarda la fecha y hora en la que es añadido un comentario
          "fields": entrada.copy()        # - Los valores importantes que queremos almacenar se guardan en el diccionario
      }
      data.append(datos_actuales) # Añade la entrada actual a la lista de datos a subir

    client.write_points(data)   # Escribe los datos en la BBDD



def main():

    # Creamos el cliente InfluxDB con la librería InfluxDBClient, aportándole los datos necesarios.
    client = InfluxDBClient(host = 'localhost', port = 8086, username = 'admin', password = 'admin', database = 'influx_db')
    client.switch_database('influx_db') # equivalente a "USE influx_db"
    scrapeo = recolectar()
    subir_metricas(client, scrapeo)

if __name__ == "__main__":
    main()
