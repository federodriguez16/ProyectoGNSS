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

def extraer_datos_rmc(trama):
    datos = trama.split(',')
    if len(datos) >= 7:
        # Latitud
        latitud = float(datos[3][:2]) + float(datos[3][2:]) / 60.0
        if datos[4] == 'S':
            latitud = -latitud
        # Longitud
        longitud = float(datos[5][:3]) + float(datos[5][3:]) / 60.0
        if datos[6] == 'W':
            longitud = -longitud
        
        velocidad= float(datos[7])*1.852
        
        return latitud, longitud, velocidad        

    return None, None

def extraer_datos_gga(trama):
    datos = trama.split(',')
    if len(datos) >= 6:
        satelites = int(datos[7])
        altitud = float(datos[9])
        
        return satelites, altitud        

    return None, None

def calcular_checksum(trama):

    # Excluir el carácter $ inicial y el * si están presentes
    if trama.startswith('$'):
        trama = trama[1:]
    if '*' in trama:
        trama = trama.split('*')[0]
    
    # Calcular el XOR de todos los caracteres
    checksum = 0
    for char in trama:
        checksum ^= ord(char)

    # Convertir a dos dígitos hexadecimales
    return f"{checksum:02X}"


# Lista para almacenar puntos de posición (latitud, longitud,velocidad)
lat = []
lon = []
vel = []
sat = []
alt = []
# 

ser = serial.Serial('/dev/ttyUSB0',baudrate=4800)

try:

    mapa = folium.Map(location=[-33.123421644558995, -64.34904595605525], zoom_start=10)  # Mapa inicial para evitar errores

    mapa.save("index.html")
    while(True):
        reading = ser.readline()
        reading = reading.decode("utf-8")
        reading = reading.replace("\r\n","")

        if reading.startswith('$GPRMC'):
                # Verificar si coincide checksum
                checksum_calculado = calcular_checksum(reading)
                checksum_original = reading.split('*')[-1]
                if checksum_calculado == checksum_original:
                    # Extraer latitud y longitud de la trama NMEA
                    latitud, longitud, velocidad = extraer_datos_rmc(reading)
                    lat.append(latitud)
                    lon.append(longitud)
                    vel.append(velocidad)
                else:
                    print("El checksum no coincide, la trama puede estar corrupta.")

        if reading.startswith('$GPGGA'):
                # Verificar si coincide checksum
                checksum_calculado = calcular_checksum(reading)
                checksum_original = reading.split('*')[-1]
                if checksum_calculado == checksum_original:
                    # Extraer cantidad de satelites y altitud de la trama NMEA
                    satelites,altitud = extraer_datos_gga(reading)
                    sat.append(satelites)
                    alt.append(altitud)    
                else:
                    print("El checksum no coincide, la trama puede estar corrupta.")
                


except KeyboardInterrupt:
    ser.close() 
    print(lat)
    print(lon)
    print(vel)
    print(sat)
    print(alt)
    print("Captura detenida por el usuario.")