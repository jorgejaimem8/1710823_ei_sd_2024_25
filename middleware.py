import requests
import os
import shutil
from typing import List

# Dirección del Webservice el cual esta en local
WEB_URL = "http://localhost:8000/generate"

# Función que lee los archivos de la carpeta en la que los inserta el cliente
# y los pasa a una lista
def leer_ficheros_directorio(directorio: str) -> List[str]:
    ficheros = os.listdir(directorio)
    
    # Filtra solo archivos .txt que tienen nombres como "0.txt", "1.txt", etc.
    ficheros_txt = [f for f in ficheros if f.endswith('.txt') and f[:-4].isdigit()]
    
    # Ordena numéricamente según el nombre (sin .txt)
    ficheros_ordenados = sorted(ficheros_txt, key=lambda x: int(x[:-4]))
    
    # Guardamos los archivos en una lista de strings
    datos = []
    for nombre in ficheros_ordenados:
        ruta = os.path.join(directorio, nombre)
        with open(ruta, 'r') as archivo:
            datos.append(archivo.read())
    return datos

# Función que envía una lista de strings al Webservice y en caso de que se
# procese correctamente la petición copia los archivos de la carpeta middleware en 
# la carpeta client para que el cliente pueda hacer la verificación del arbol
def enviar_datos_a_webservice(datos):
    # Generamos petición POST al Webservice para que cree el arbol con nuestros datos
    response = requests.post(WEB_URL, json={"datos": datos})
    # Si la petición es exitosa, creamos la carpeta client si no existe para guardar los archivos
    # y copiamos los archivos en las carpeta middleware a client
    if response.status_code == 200:
        print("Webservice procesó correctamente los datos.")
        if not os.path.exists("client"):
            os.makedirs("client")
        for i in range(len(datos)):
            shutil.copy(f"middleware/{i}.txt", f"client/{i}.txt")
    else:
        print("Error en el Webservice:", response.json())

# Función principal que lee los archivos enviados por el cliente, 
# y los guarda en una lista de strings para enviarlos al Webservice
if __name__ == "__main__":
    carpeta = "client_entry"
    datos = leer_ficheros_directorio(carpeta)
    enviar_datos_a_webservice(datos)
