import requests

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