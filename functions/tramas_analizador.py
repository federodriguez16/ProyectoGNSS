# Funciones para extraer los datos provenientes por el GPS

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
        
        velocidad= round(float(datos[7])*1.852, 2)
        
        return latitud, longitud, velocidad        

    return None, None , None

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

def obtener_serial(ser):
    reading = ser.readline()
    reading = reading.decode("utf-8")
    reading = reading.replace("\r\n","")

    return reading
