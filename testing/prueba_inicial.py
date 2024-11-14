#Codigo del machiner(GPT)

import serial
import folium
import time
import numpy as np
from scipy.interpolate import interp1d

# Configuración del puerto serial (ajustar según el puerto y velocidad de baudios)
# puerto = 'COM3'  # Cambia esto según el puerto correcto en tu PC
# velocidad_baude = 9600

# Tramas NMEA GGA de ejemplo para simular la recepción de datos en tiempo real
tramas = [
    "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47",
    "$GPGGA,123520,4807.048,N,01131.010,E,1,08,0.9,545.4,M,46.9,M,,*47",
    "$GPGGA,123521,4807.058,N,01131.020,E,1,08,0.9,545.4,M,46.9,M,,*47",
    "$GPGGA,123522,4807.068,N,01131.030,E,1,08,0.9,545.4,M,46.9,M,,*47",
    "$GPGGA,123523,4807.078,N,01131.040,E,1,08,0.9,545.4,M,46.9,M,,*47"
]

# Lista para almacenar puntos de posición (latitud, longitud)
posiciones = []

# Función para extraer latitud y longitud de la trama NMEA GGA
def extraer_lat_lon(trama):
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

# Inicializar el mapa
mapa = folium.Map(location=[48.1173, 11.5167], zoom_start=15)

# Función para actualizar el mapa con interpolación
def actualizar_mapa_con_interpolacion():
    # Crear arrays de latitud y longitud a partir de los puntos capturados
    latitudes = np.array([p[0] for p in posiciones])
    longitudes = np.array([p[1] for p in posiciones])

    # Interpolación de los puntos
    if len(latitudes) > 2:
        # Crear una interpolación lineal entre los puntos capturados
        f_lat = interp1d(np.arange(len(latitudes)), latitudes, kind='linear')
        f_lon = interp1d(np.arange(len(longitudes)), longitudes, kind='linear')

        # Definir puntos interpolados
        puntos_interpolados = 10  # Número de puntos interpolados entre cada par de posiciones
        indices_interpolados = np.linspace(0, len(latitudes) - 1, num=len(latitudes) * puntos_interpolados)

        latitudes_interpoladas = f_lat(indices_interpolados)
        longitudes_interpoladas = f_lon(indices_interpolados)

        # Agregar la ruta interpolada al mapa
        folium.PolyLine(list(zip(latitudes_interpoladas, longitudes_interpoladas)), color="blue").add_to(mapa)

# Simulación de la captura en tiempo real
for trama in tramas:
    # Extraer latitud y longitud de la trama NMEA
    latitud, longitud = extraer_lat_lon(trama)
    if latitud is not None and longitud is not None:
        posiciones.append((latitud, longitud))
        folium.Marker([latitud, longitud], tooltip="Posición capturada").add_to(mapa)

        # Actualizar mapa con la trayectoria interpolada
        actualizar_mapa_con_interpolacion()

        # Guardar el mapa en un archivo HTML en cada actualización
        mapa.save("mi_posicion_trayectoria.html")
        print("Mapa actualizado y guardado como 'mi_posicion_trayectoria.html'")

        # Simular el tiempo real con una breve pausa
        time.sleep(1)
