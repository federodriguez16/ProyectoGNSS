import folium
import serial
import time
from folium.plugins import MiniMap

# Documentación: https://python-visualization.github.io/folium/latest/index.html

# https://python-visualization.github.io/folium/latest/advanced_guide/flask.html

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

i=0
coordenadas = []

ser = serial.Serial('/dev/ttyUSB0',baudrate=4800)

while(1):
        reading = ser.readline()
        reading = reading.decode("utf-8")
        reading = reading.replace("\r\n","")

        if reading.startswith('$GPGGA'):
                # Extraer latitud y longitud de la trama NMEA
                latitud, longitud = extraer_datos(reading)
                coordenadas.append([latitud,longitud])               

                # Create the map and add the line
                m = folium.Map(location=[coordenadas[0][0], coordenadas[0][1]], zoom_start=20)
                
                MiniMap(toggle_display=True).add_to(m)

                folium.PolyLine(
                    locations=coordenadas,
                    color="#FF0000",
                    weight=3,
                    tooltip="Trayecto recorrido",
                ).add_to(m)

                

                folium.Marker([coordenadas[-1][0],coordenadas[-1][1]], tooltip="Última posición").add_to(m)

                m.save('index.html')
                print('Mapa Actualizado')
                time.sleep(3)

# Mapa inicial para evitar errores

#mapa = folium.Map(location=[latitud,longitud], zoom_start=15)  

#mapa.save("index.html")

