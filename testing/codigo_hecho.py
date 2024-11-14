#Error en obtencion de muestras y generacion de mapa.HTML

import serial, time
import folium
import numpy as np
from scipy.interpolate import interp1d
from flask import Flask, render_template_string

app = Flask(__name__)

# Configuración del puerto serial
puerto = '/dev/ttyUSB0'  # Cambia esto según el puerto correcto en tu sistema
velocidad_baude = 4800

# Lista para almacenar puntos de posición
posiciones = []

# Plantilla HTML básica para mostrar el mapa
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="60"> <!-- Refrescar cada 5 segundos -->
    <title>Mapa en Tiempo Real</title>
</head>
<body>
    <h1>Mapa en Tiempo Real</h1>
    <iframe src="/mapa" width="100%" height="500"></iframe>
</body>
</html>
"""

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

# Función para actualizar el mapa con interpolación
def actualizar_mapa():
    mapa = folium.Map(location=[-33.123421644558995, -64.34904595605525], zoom_start=10)  # Mapa inicial para evitar errores

    # Crear arrays de latitud y longitud a partir de los puntos capturados
    latitudes = np.array([p[0] for p in posiciones])
    longitudes = np.array([p[1] for p in posiciones])

    if len(latitudes) > 2:
        f_lat = interp1d(np.arange(len(latitudes)), latitudes, kind='linear')
        f_lon = interp1d(np.arange(len(longitudes)), longitudes, kind='linear')
        puntos_interpolados = 10
        indices_interpolados = np.linspace(0, len(latitudes) - 1, num=len(latitudes) * puntos_interpolados)

        latitudes_interpoladas = f_lat(indices_interpolados)
        longitudes_interpoladas = f_lon(indices_interpolados)

        folium.PolyLine(list(zip(latitudes_interpoladas, longitudes_interpoladas)), color="blue").add_to(mapa)

    if posiciones:
        folium.Marker([latitudes[-1], longitudes[-1]], tooltip="Última posición").add_to(mapa)

    # Guardar el archivo HTML en la carpeta 'static'
    mapa.save("static/mapa.html")

# Ruta para servir el mapa HTML
@app.route('/mapa')
def mostrar_mapa():
    return open("static/mapa.html").read()

# Página principal para ver el mapa en tiempo real
@app.route('/')
def index():
    return render_template_string(html_template)

# Leer del puerto serial y actualizar el mapa en tiempo real
def leer_datos_serial():
    with serial.Serial(puerto, velocidad_baude) as ser:
        while True:
            linea = ser.readline().decode('ascii', errors='replace')
            if linea.startswith('$GPGGA'):
                latitud, longitud = extraer_lat_lon(linea)
                if latitud is not None and longitud is not None:
                    posiciones.append((latitud, longitud))
                    actualizar_mapa()

if __name__ == "__main__":
    import threading

    # Ejecutar la función de lectura de datos en un hilo separado
    hilo_serial = threading.Thread(target=leer_datos_serial, daemon=True)
    hilo_serial.start()

    # Ejecutar el servidor Flask en modo de desarrollo
    app.run(debug=True)
