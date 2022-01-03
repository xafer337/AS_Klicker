#!/usr/bin/env python3
from influxdb import InfluxDBClient
from datetime import datetime
import enum
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
        print (metricas[i])
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
    i = 1    
    while i <= len(array)-1:
        if array[i] != '':
            if i != 3:
                if 'MiB' in array[i] or 'GiB' in array[i] or 'MB' in array[i] or 'kB' in array[i]:
                    numero,unidad=separar(array[i])                    
                    numero_convertido = conversion(numero,unidad)
                    array_limpio.append(numero_convertido)
                else:
                    dato = re.findall(r'-?\d+\.?\d*',array[i])
                    if dato:
                        array_limpio.append(dato.pop())                    
            else:
                array_limpio.append(array[i])
        i+=1
    return array_limpio

def conversion(numero, unidad):
    if unidad == 'MiB':
        return float(numero)*(1.049*(10**6))
    elif unidad =='GiB':
        return float(numero)*(1.074*(10**9))
    elif unidad =='MB':
        return float(numero)*1000000
    elif unidad =='kB':
        return float(numero)*1000

def separar(string):
    #dado un numero con su respectiva unidad lo separa; ejemplo: 11.63MiB --> (11.63,MiB)
    for i,c in enumerate(string):
        if not c.isdigit() and c != '.':
            break
    num = string[:i]
    unit = string[i:]
    return (num,unit)
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
