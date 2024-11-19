#Importamos las Librerias a Utilizar

import threading
import serial
import folium
import time
from functions.api import obtener_datos_tiempo
from functions.tramas_analizador import *
from flask import Flask, render_template

# Seleccionamos el dispositivo serial a Capturar

ser = serial.Serial('/dev/ttyUSB0',baudrate=4800)

# Listas para almacenar puntos de posición (latitud, longitud,velocidad)

lat = []
lon = []
vel = []
sat = []
alt = []

# Variables Auxiliares

flag = 1

#Definimos nuestra aplicacion flask

app = Flask(__name__)

# Creamos nuestra funcion que siempre estara tomando datos

def obtener_informacion(lat,lon):
    while(True):
        reading = obtener_serial(ser)
        if reading.startswith('$GPRMC'):
            # Verificar si coincide checksum
            checksum_calculado = calcular_checksum(reading)
            checksum_original = reading.split('*')[-1]
            if checksum_calculado == checksum_original:
                # Extraer latitud longitud y velocidad de la trama NMEA
                latitud, longitud, velocidad = extraer_datos_rmc(reading)
                lat.append(latitud)
                lon.append(longitud)
                vel.append(velocidad)
            else:
                print("El checksum no coincide, la trama RMC esta corrupta.")

# Pagina Principal

@app.route('/')
def index():

    # Llamamos a nuestra funcion en un hilo separado para que ejecute independientemente del programa

    global flag

    while(flag == 1):
        thread = threading.Thread(target=obtener_informacion, args=(lat, lon))
        thread.start()
        time.sleep(3)
        flag = 0


    # Con la Ubicación obtenida, mandamos estos datos a la API para que nos de valores de tiempo

    datos = obtener_datos_tiempo(lat[-1],lon[-1])

    informacion = {
        "locacion": f"{str(datos['location']['name'])}, {str(datos['location']['region'])}, {str(datos['location']['country'])}",
        "temperatura": str(datos['current']['temp_c']) + "°C",
        "humedad": str(datos['current']['humidity']) + "%",
        "precipitaciones": str(datos['current']['precip_mm']),
        "presion": str(datos['current']['pressure_mb']),
        "estado": str(datos['current']['condition']['text']),
        "icono": "http://" + str(datos['current']['condition']['icon'])
    }

    return render_template('index.html', datos=informacion)

if __name__ == '__main__':
    app.run(debug=True)