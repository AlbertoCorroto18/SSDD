#!/usr/bin/python3
# ------------------------------------------------------------
# Servidor UDP que recibe dos enteros de un cliente, los suma
# y devuelve el resultado. El servidor permanece activo 
# indefinidamente, escuchando peticiones.
# ------------------------------------------------------------

import socket   # Librería para crear sockets
import struct   # Librería para empaquetar/desempaquetar datos binarios

# Puerto en el que escuchará el servidor
PORT = 10001

# Crear un socket UDP (AF_INET = IPv4, SOCK_DGRAM = UDP)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # Enlazar el socket a todas las interfaces ('') y al puerto especificado
    s.bind(('', PORT))
    print(f"Servidor UDP escuchando en el puerto {PORT}...")

    # Bucle infinito: el servidor no se detiene
    while True:
        print("\nEsperando solicitud del cliente...")

        # Recibir datos (máximo 1024 bytes) y la dirección del cliente
        data, client = s.recvfrom(1024)
        print(f"Datos recibidos de {client}")

        # Desempaquetar los dos enteros de 4 bytes cada uno (big endian)
        num1, num2 = struct.unpack("!ii", data)
        print(f"Numeros recibidos: {num1}, {num2}")

        # Calcular la suma
        result = num1 + num2

        # Empaquetar el resultado (entero de 4 bytes) y enviarlo de vuelta
        s.sendto(struct.pack('!i', result), client)
        print(f"Enviado a {client}: {num1} + {num2} = {result}")
