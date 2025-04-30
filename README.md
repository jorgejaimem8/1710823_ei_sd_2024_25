# Jorge Modrego, Engenharia Informática, 1710823
## Sistemas Distribuidos 

Verificador de Inclusión de Datos en Árboles de Merkle:

Este proyecto implementa un sistema distribuido para construir árboles de Merkle a partir de datos proporcionados, generar pruebas de inclusión y verificarlas posteriormente. El sistema está compuesto por tres módulos principales:

webservice.py: Servicio web que construye el árbol de Merkle y genera archivos de inclusión.

middleware.py: Cliente intermedio que prepara los datos y los envía al servicio web.

client.py: Cliente final que verifica la validez de los datos y su inclusión en el árbol.




Requisitos

Python 3.8 o superior

fastapi

uvicorn

requests

Puedes instalar las dependencias necesarias ejecutando:
pip install fastapi uvicorn requests






Estructura del Proyecto:

-webservice.py        Servicio web (FastAPI)
-middleware.py        Cliente intermedio
-client.py            Cliente final

-client_entry/        Carpeta con datos de entrada
-middleware/          Carpeta generada con archivos de inclusión
-client/              Carpeta generada para verificación





Ejecución del Proyecto:



1. Iniciar el Webservice

Ejecuta el servicio web en un puerto local (por ejemplo, 8000):

uvicorn webservice:app --reload


2. Preparar los Datos
Crea una carpeta llamada client_entry/ y añade archivos .txt con los datos que deseas verificar. La cantidad de archivos debe ser una potencia de 2 (por ejemplo, 2, 4, 8...).

Ejemplo:

client_entry/
-0.txt
-1.txt
-2.txt
-3.txt
Cada archivo debe contener un único string/plano de datos.



3. Ejecutar el Middleware
El middleware lee los archivos desde client_entry/, envía los datos al webservice, y copia los archivos de inclusión generados a la carpeta client/.
ESTOS DEBEN LLAMARSE: 0.txt, 1.txt...,7.txt,...,2^n-1.txt

python middleware.py




4. Verificar Inclusión
El cliente lee los archivos en la carpeta client/ y verifica si cada dato está correctamente incluido en el árbol de Merkle, siguiendo el camino de verificación y comparando con la raíz.

python client.py

Se mostrará por consola el resultado de la verificación para cada archivo.

