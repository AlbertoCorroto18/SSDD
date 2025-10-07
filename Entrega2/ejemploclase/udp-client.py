#!/usr/bin/env python3
# ------------------------------------------------------------
# CLIENTE UDP DE SENSOR
# ------------------------------------------------------------
# - Crea un socket UDP.
# - Genera un mensaje protobuf (Reading) con datos del sensor.
# - Lo serializa a bytes y lo envía al servidor.
# ------------------------------------------------------------

import sys
import socket
import sensor_pb2   # Módulo generado a partir de sensor.proto

# ------------------------------------------------------------
# Comprobación de argumentos
# ------------------------------------------------------------
if len(sys.argv) < 2:
    print('Usage: ./udp-client.py <host>')
    exit()

# ------------------------------------------------------------
# Crear socket UDP
# ------------------------------------------------------------
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
destination = (sys.argv[1], 1234)   # Dirección y puerto destino

# ------------------------------------------------------------
# Crear un mensaje protobuf de tipo Reading
# ------------------------------------------------------------
reading = sensor_pb2.Reading()
reading.Id = 1                                # ID del sensor
reading.type = sensor_pb2.Reading.HUMIDITY    # Tipo: humedad
reading.value = 0.2                           # Valor medido
reading.unit = "kg/m3"                        # Unidad de medida

# ------------------------------------------------------------
# Serializar el mensaje a bytes
# ------------------------------------------------------------
data = reading.SerializeToString()
print(data)  # Muestra los bytes en crudo (solo para depurar)

# ------------------------------------------------------------
# Enviar los datos al servidor
# ------------------------------------------------------------
sock.sendto(data, destination)

# ------------------------------------------------------------
# Cerrar el socket
# ------------------------------------------------------------
sock.close()
