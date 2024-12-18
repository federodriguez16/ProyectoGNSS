# Importamos las Librerias a Utilizar

import threading
import serial
import folium
import argparse
from functions.api import obtener_datos_tiempo
from functions.tramas_analizador import *
from flask import Flask, render_template

# Seleccionamos el dispositivo serial a Capturar

ser = serial.Serial('/dev/ttyUSB0',baudrate=4800)

parser = argparse.ArgumentParser(description="Descripción del script")

parser.add_argument("api_key", help="key from weatherapi")  # Obligatorio

args = parser.parse_args()

# Listas para almacenar puntos de posición (latitud, longitud,velocidad)

lat = []
lon = []
coordenadas = []

#Definimos nuestra aplicacion flask

app = Flask(__name__)

# Creamos nuestra funcion que siempre estar tomando datos

def obtener_informacion(lat,lon,coordenadas):
    while(True):
        global sat
        global alt
        global vel
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
                vel = velocidad
                coordenadas.append([latitud,longitud])
            else:
                print("El checksum no coincide, la trama RMC esta corrupta.")
        if reading.startswith('$GPGGA'):
            satelites, altitud = extraer_datos_gga(reading)
            sat = satelites
            alt = altitud

thread = threading.Thread(target=obtener_informacion, args=(lat, lon, coordenadas))
thread.start()

# Pagina Principal

@app.route('/')
def index():

    # Llamamos a nuestra funcion en un hilo separado para que ejecute independientemente del programa


    # Añadimos el mapa que vamos a utilizar para el seguimiento

    map = folium.Map(location=[lat[-1], lon[-1]], zoom_start=17,control_scale=True)

    folium.PolyLine(locations=coordenadas, color="#FF0000", weight=3, tooltip="Trayecto recorrido").add_to(map)

    folium.Marker([lat[-1], lon[-1]], tooltip="Última posición").add_to(map)

    # Creamos el iframe que se colocara en la Pagina

    map.get_root().width = "100%"
    map.get_root().height = "600px"
    iframe = map.get_root()._repr_html_()

    # Con la Ubicación obtenida, mandamos estos datos a la API para que nos de valores de tiempo

    datos = obtener_datos_tiempo(lat[-1],lon[-1],args.api_key)

    informacion = {
        "locacion": f"{str(datos['location']['name'])}, {str(datos['location']['region'])}, {str(datos['location']['country'])}",
        "temperatura": str(datos['current']['temp_c']) + "°C",
        "humedad": str(datos['current']['humidity']) + "%",
        "precipitaciones": str(datos['current']['precip_mm']) + " mm",
        "presion": str(datos['current']['pressure_mb']) + " mb",
        "estado": str(datos['current']['condition']['text']),
        "icono": "http://" + str(datos['current']['condition']['icon']),
        "velocidad": str(vel) + " km/h",
        "satelites": str(sat),
        "altitud": str(alt) + " m"
    }

    return render_template('index.html', datos=informacion,iframe=iframe)

if __name__ == '__main__':
    app.run(debug=True)