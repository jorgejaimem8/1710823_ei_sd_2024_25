import hashlib
import os

def hash_function(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verificar_inclusion(file_path: str):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()

    dato = lines[0].split(": ")[1]
    dato_hash = hash_function(dato.encode())
    dato_hash_esperado = lines[1].split(": ")[1]

    # Verificamos que el dato no haya sido manipulado
    if dato_hash != dato_hash_esperado:
        print(f"❌ El dato '{dato}' NO coincide con el hash registrado.")
        return

    camino = lines[3:-1]
    raiz_esperada = lines[-1].split(": ")[1]

    actual_hash = dato_hash
    for linea in camino:
        h, direccion = linea.split(',')
        if direccion == 'left':
            actual_hash = hash_function((h + actual_hash).encode())
        else:
            actual_hash = hash_function((actual_hash + h).encode())

    if actual_hash == raiz_esperada:
        print(f"✅ El dato '{dato}' está incluido.")
    else:
        print(f"❌ El dato '{dato}' NO está incluido.")

if __name__ == "__main__":
    carpeta_cliente = "client"
    for fichero in sorted(os.listdir(carpeta_cliente)):
        print(f"Verificando: {fichero}")
        verificar_inclusion(os.path.join(carpeta_cliente, fichero))
        print("-")
