#!/usr/bin/env python3
# ------------------------------------------------------------
# SERVIDOR UDP DE SENSOR
# ------------------------------------------------------------
# - Escucha en el puerto 1234.
# - Recibe mensajes protobuf (Reading) de distintos sensores.
# - Deserializa el mensaje y muestra sus valores de forma legible.
# ------------------------------------------------------------

import socket
from sensor_pb2 import Reading   # Importamos solo la clase Reading

# ------------------------------------------------------------
# Crear socket UDP y vincularlo al puerto 1234
# ------------------------------------------------------------
sock = socket.socket(type=socket.SOCK_DGRAM)
sock.bind(('', 1234))  # '' = escuchar en todas las interfaces

# Crear una instancia del mensaje para reutilizarla
reading = Reading()

# ------------------------------------------------------------
# Bucle principal (escucha permanente)
# ------------------------------------------------------------
while True:
    # Recibir datos de hasta 1024 bytes y dirección del cliente
    data, address = sock.recvfrom(1024)
    print(f"Sensor conectado: {address}\nDatos crudos:\n{data}")

    # --------------------------------------------------------
    # Deserializar los bytes en un objeto Reading
    # --------------------------------------------------------
    reading.ParseFromString(data)

    # --------------------------------------------------------
    # Mostrar información de forma legible
    # --------------------------------------------------------
    print("Sensor {0.Id} ({1}) valor: {0.value:.2f} {0.unit}".format(
        reading, Reading.SensorType.Name(reading.type)))
