import json
import os

CREDENCIALES_FILE = 'credenciales.json'

def guardar_credenciales(username, password):
    """Guardar las credenciales en un archivo JSON"""
    credenciales = {
        'username': username,
        'password': password
    }

    with open(CREDENCIALES_FILE, 'w') as f:
        json.dump(credenciales, f)
    print(f"Credenciales guardadas en {CREDENCIALES_FILE}.")

def cargar_credenciales():
    """Cargar las credenciales desde el archivo JSON"""
    if os.path.exists(CREDENCIALES_FILE):
        with open(CREDENCIALES_FILE, 'r') as f:
            credenciales = json.load(f)
            return credenciales
    return None

def eliminar_credenciales():
    """Eliminar el archivo de credenciales"""
    if os.path.exists(CREDENCIALES_FILE):
        os.remove(CREDENCIALES_FILE)
        print(f"Archivo {CREDENCIALES_FILE} eliminado.")
    else:
        print(f"El archivo {CREDENCIALES_FILE} no existe.")
