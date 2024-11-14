import serial
import folium
import time
import requests

# Funcion obtencion datos del tiempo

def tiempo(lat,lon):

    API_KEY = '2367a071311c47f684d211141230207'
    URL = 'http://api.weatherapi.com/v1/current.json'

    latitud = -33.123421644558995
    longitud = -64.34904595605525

    datos = str(latitud) + ',' +  str(longitud)

    parametros = {'key': API_KEY, 'q':datos}

    response = requests.get(URL,parametros)
    # print(response.status_code)
    dato = response.json()
    # print(type(dato))

    print('Ciudad: ' + str(dato['location']['name']))
    print('Temperatura Actual: ' + str(dato['current']['temp_c']))
    print('Sensacion Termica: ' + str(dato['current']['feelslike_c']))
    print('Humedad: ' + str(dato['current']['humidity']))
    print('Precipitaciones: ' + str(dato['current']['precip_mm']))
    print('Presion: ' + str(dato['current']['pressure_mb']))

# Funcion para extraer los datos provenientes por el GPS

def extraer_datos(trama):
    datos = trama.split(',')
    if len(datos) >= 6:
        # Latitud
        latitud = float(datos[2][:2]) + float(datos[2][2:]) / 60.0
        if datos[3] == 'S':
            latitud = -latitud
        # Longitud
        longitud = float(datos[4][:3]) + float(datos[4][3:]) / 60.0
        if datos[5] == 'W':
            longitud = -longitud
        return latitud, longitud
    return None, None


# Lista para almacenar puntos de posición (latitud, longitud)
lat = []
lon = []

# 

ser = serial.Serial('/dev/ttyUSB0',baudrate=4800)

try:

    mapa = folium.Map(location=[-33.123421644558995, -64.34904595605525], zoom_start=10)  # Mapa inicial para evitar errores

    mapa.save("index.html")
    while(True):
        reading = ser.readline()
        reading = reading.decode("utf-8")
        reading = reading.replace("\r\n","")

        if reading.startswith('$GPGGA'):
                # Extraer latitud y longitud de la trama NMEA
                latitud, longitud = extraer_datos(reading)
                lat.append(latitud)
                lon.append(longitud)

except KeyboardInterrupt:
    ser.close() 
    print(lat)
    print(lon)
    print("Captura detenida por el usuario.")