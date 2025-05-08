import cherrypy
import hashlib
import os
import json

# Función de hash SHA-256
def hash_function(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

# Genera el árbol, nivel por nivel, combinando hashes adyacentes.
def build_merkle_tree(leaves):
    tree = [list(map(lambda d: hash_function(d.encode()), leaves))]
    while len(tree[-1]) > 1:
        level = []
        current_level = tree[-1]
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1]
            parent_hash = hash_function((left + right).encode())
            level.append(parent_hash)
        tree.append(level)
    return tree

# Calcula el camino de verificación para cada dato (es decir, 
# los hashes de los nodos hermanos necesarios para reconstruir la raíz).
def get_merkle_path(tree, index):
    path = []
    for level in tree[:-1]:
        sibling_index = index ^ 1
        if sibling_index < len(level):
            direction = 'left' if sibling_index < index else 'right'
            path.append((level[sibling_index], direction))
        index //= 2
    return path

# Servicio web RESTful con CherryPy que acepta entradas con formato JSON
class MerkleWebService:

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def generate(self):
        input_data = cherrypy.request.json
        datos = input_data.get("datos", [])

        if len(datos) == 0 or (len(datos) & (len(datos) - 1)) != 0:
            cherrypy.response.status = 400
            return {"error": "Debe proporcionar 2^n elementos."}

        output_dir = "middleware"
        os.makedirs(output_dir, exist_ok=True)

        tree = build_merkle_tree(datos)
        root = tree[-1][0]

        for i, dato in enumerate(datos):
            path = get_merkle_path(tree, i)
            file_path = os.path.join(output_dir, f"{i}.txt")
            with open(file_path, "w") as f:
                f.write(f"Dato original: {dato}\n")
                f.write(f"Hash del dato: {hash_function(dato.encode())}\n")
                f.write("Camino hacia la raíz (hash,direccion):\n")
                for h, dir in path:
                    f.write(f"{h},{dir}\n")
                f.write(f"Hash raíz: {root}\n")

        return {
            "status": "OK",
            "hash_raiz": root,
            "archivos_generados": len(datos)
        }

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080
    })
    cherrypy.quickstart(MerkleWebService())
