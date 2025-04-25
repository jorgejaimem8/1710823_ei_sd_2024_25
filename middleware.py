import requests
import os
import shutil
from typing import List

WEB_URL = "http://localhost:8000/generate"

def leer_ficheros_directorio(directorio: str) -> List[str]:
    ficheros = os.listdir(directorio)
    
    # Filtra solo archivos .txt que tienen nombres como "0.txt", "1.txt", etc.
    ficheros_txt = [f for f in ficheros if f.endswith('.txt') and f[:-4].isdigit()]
    
    # Ordena numéricamente según el nombre (sin .txt)
    ficheros_ordenados = sorted(ficheros_txt, key=lambda x: int(x[:-4]))
    
    datos = []
    for nombre in ficheros_ordenados:
        ruta = os.path.join(directorio, nombre)
        with open(ruta, 'r') as archivo:
            datos.append(archivo.read())
    return datos


def enviar_datos_a_webservice(datos):
    response = requests.post(WEB_URL, json={"datos": datos})
    if response.status_code == 200:
        print("✅ Webservice procesó correctamente los datos.")
        if not os.path.exists("cliente"):
            os.makedirs("cliente")
        for i in range(len(datos)):
            shutil.copy(f"middleware/{i}.txt", f"client/{i}.txt")
    else:
        print("❌ Error en el Webservice:", response.json())

if __name__ == "__main__":
    carpeta = "client_entry"
    datos = leer_ficheros_directorio(carpeta)
    enviar_datos_a_webservice(datos)
