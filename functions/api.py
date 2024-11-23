import requests

API_KEY = '2367a071311c47f684d211141230207'
URL = 'http://api.weatherapi.com/v1/current.json'


def obtener_datos_tiempo(latitud,longitud):

    datos = str(latitud) + ',' +  str(longitud)

    parametros = {'key': API_KEY, 'q':datos}

    response = requests.get(URL,parametros)
    # print(response.status_code)
    datos = response.json()

    return datos