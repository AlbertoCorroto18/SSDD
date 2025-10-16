#!/usr/bin/env python3
# Ejemplo basado en la guía oficial de Flask-RESTful:
# https://flask-restful.readthedocs.io/en/latest/quickstart.html

from flask import Flask, request
from flask_restful import Resource, Api, abort

# ------------------------------------------------------------
# Inicialización de la aplicación y API
# ------------------------------------------------------------
app = Flask(__name__)
api = Api(app)

# "Base de datos" en memoria (diccionario)
devices = {
    'switch1': 'enabled',
    'light1': 'disabled',
}

# ------------------------------------------------------------
# Clase Resource: dispositivo individual (/switch1, /light1, etc.)
# ------------------------------------------------------------
class Device(Resource):
    def get(self, device_id):
        # Devuelve el estado del dispositivo si existe
        if device_id not in devices:
            abort(404)                     # Error HTTP 404 si no existe
        return {device_id: devices.get(device_id)}  # Respuesta JSON

    def put(self, device_id):
        # Actualiza/crea un dispositivo: recibe "status" vía formulario
        devices[device_id] = request.form['status']
        return {device_id: devices[device_id]}      # Respuesta JSON

# ------------------------------------------------------------
# Clase Resource: lista completa de dispositivos (/)
# ------------------------------------------------------------
class DeviceList(Resource):
    def get(self):
        # Devuelve todos los dispositivos y sus estados
        return devices

# ------------------------------------------------------------
# Registro de recursos en la API
# ------------------------------------------------------------
api.add_resource(DeviceList, '/')                 # GET /
api.add_resource(Device, '/<string:device_id>')   # GET /id  PUT /id

# ------------------------------------------------------------
# Punto de entrada principal
# ------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)   # Ejecuta servidor en localhost:5000
