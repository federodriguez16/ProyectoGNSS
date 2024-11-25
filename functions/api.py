import requests

URL = 'http://api.weatherapi.com/v1/current.json'


def obtener_datos_tiempo(latitud,longitud,api_key):

    datos = str(latitud) + ',' +  str(longitud)

    parametros = {'key': str(api_key), 'q':datos}

    response = requests.get(URL,parametros)
    # print(response.status_code)
    datos = response.json()

    return datos