from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
import hashlib
import os

app = FastAPI()

class DataInput(BaseModel):
    datos: List[str]

# Función de hash (SHA-256)
def hash_function(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

# Construye el árbol de Merkle completo
def build_merkle_tree(leaves: List[str]) -> List[List[str]]:
    tree = [list(map(lambda d: hash_function(d.encode()), leaves))]
    while len(tree[-1]) > 1:
        level = []
        current_level = tree[-1]
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1]
            parent_hash = hash_function((left + right).encode())
            level.append(parent_hash)
        tree.append(level)
    return tree

# Genera el camino hasta la raíz para un índice dado
def get_merkle_path(tree: List[List[str]], index: int) -> List[Tuple[str, str]]:
    path = []
    for level in tree[:-1]:
        sibling_index = index ^ 1
        if sibling_index < len(level):
            direction = 'left' if sibling_index < index else 'right'
            path.append((level[sibling_index], direction))
        index //= 2
    return path

# Endpoint principal
@app.post("/generate")
def generate_inclusion_files(input_data: DataInput):
    data = input_data.datos

    # Verifica que el número de datos sea potencia de 2
    if len(data) == 0 or (len(data) & (len(data)-1)) != 0:
        raise HTTPException(status_code=400, detail="Debe proporcionar 2^n elementos.")

    # Directorio de salida
    output_dir = "middleware"
    os.makedirs(output_dir, exist_ok=True)

    # Construcción del árbol de Merkle
    tree = build_merkle_tree(data)
    root = tree[-1][0]

    # Creación de los ficheros individuales con los datos necesarios
    # para el arbol de Merkle
    for i, dato in enumerate(data):
        path = get_merkle_path(tree, i)
        file_path = os.path.join(output_dir, f"{i}.txt")
        with open(file_path, "w") as f:
            f.write(f"Dato original: {dato}\n")
            f.write(f"Hash del dato: {hash_function(dato.encode())}\n")
            f.write("Camino hacia la raíz (hash,direccion):\n")
            for h, dir in path:
                f.write(f"{h},{dir}\n")
            f.write(f"Hash raíz: {root}\n")

    # Respuesta JSON del endpoint
    return {
        "status": "OK",
        "hash_raiz": root,
        "archivos_generados": len(data)
    }
