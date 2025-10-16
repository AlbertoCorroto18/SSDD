#!/usr/bin/env python3
# Cliente de ejemplo para probar la API Flask-RESTful.

import requests   # Librería HTTP para enviar peticiones al servidor

BASE_URL = "http://127.0.0.1:5000"   # Dirección del servidor Flask

def run():
    # ----------------------------------------------------------
    # GET general → lista todos los dispositivos
    # ----------------------------------------------------------
    print("GET /  → lista de dispositivos")
    r = requests.get(f"{BASE_URL}/")
    print(r.status_code, r.json())

    # ----------------------------------------------------------
    # GET individual → obtener estado de un dispositivo
    # ----------------------------------------------------------
    print("\nGET /switch1  → estado de switch1")
    r = requests.get(f"{BASE_URL}/switch1")
    print(r.status_code, r.json() if r.status_code == 200 else r.text)

    # ----------------------------------------------------------
    # PUT → actualizar el estado de un dispositivo existente
    # ----------------------------------------------------------
    print("\nPUT /switch1  → actualizar a 'disabled'")
    r = requests.put(f"{BASE_URL}/switch1", data={'status': 'disabled'})
    print(r.status_code, r.json())

    # ----------------------------------------------------------
    # GET /switch1 nuevamente para comprobar cambio
    # ----------------------------------------------------------
    print("\nGET /switch1 (después del PUT)")
    r = requests.get(f"{BASE_URL}/switch1")
    print(r.status_code, r.json())

    # ----------------------------------------------------------
    # PUT → crear un nuevo dispositivo (por ejemplo, sensor1)
    # ----------------------------------------------------------
    print("\nPUT /sensor1  → crear nuevo dispositivo habilitado")
    r = requests.put(f"{BASE_URL}/sensor1", data={'status': 'enabled'})
    print(r.status_code, r.json())

    # ----------------------------------------------------------
    # GET /  → lista actualizada de dispositivos
    # ----------------------------------------------------------
    print("\nGET / (lista actualizada)")
    r = requests.get(f"{BASE_URL}/")
    print(r.status_code, r.json())

if __name__ == '__main__':
    run()
