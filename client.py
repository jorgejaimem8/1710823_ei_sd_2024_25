import hashlib
import os

# función para calcular el hash SHA-256 de un dato
def hash_function(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

# función para verificar la inclusión de un dato en el árbol de Merkle
def verificar_inclusion(file_path: str):
    # Verificamos que el archivo exista
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()

    # Cogemos el valor original
    dato = lines[0].split(": ")[1]

    # Hasheamos el valor original
    dato_hash = hash_function(dato.encode())

    # Cogemos el valor del hash que se nos proporciona en el fichero
    dato_hash_esperado = lines[1].split(": ")[1]

    # Verificamos que el dato no haya sido manipulado
    if dato_hash != dato_hash_esperado:
        print(f"El dato '{dato}' NO coincide con el hash registrado.")
        return

    # Extraemos el camino de verificación
    camino = lines[3:-1]

    # Extraemos la raiz esperada
    raiz_esperada = lines[-1].split(": ")[1]

    # Calculamos el hash de la raíz a partir del camino
    actual_hash = dato_hash
    for linea in camino:
        h, direccion = linea.split(',')
        if direccion == 'left':
            actual_hash = hash_function((h + actual_hash).encode())
        else:
            actual_hash = hash_function((actual_hash + h).encode())

    # Verificamos si el hash calculado coincide con la raíz esperada
    if actual_hash == raiz_esperada:
        print(f"El dato '{dato}' está incluido.")
    else:
        print(f"El dato '{dato}' NO está incluido.")

# Función principal para verificar todos los archivos en el directorio
if __name__ == "__main__":
    carpeta_cliente = "client"
    for fichero in sorted(os.listdir(carpeta_cliente)):
        print(f"Verificando: {fichero}")
        verificar_inclusion(os.path.join(carpeta_cliente, fichero))
        print("-")
