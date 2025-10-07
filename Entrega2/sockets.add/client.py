#!/usr/bin/python3
# ------------------------------------------------------------
# Cliente UDP que envía dos enteros al servidor, recibe 
# el resultado de su suma y lo muestra por pantalla.
# ------------------------------------------------------------

import socket   # Librería para manejar conexiones de red
import struct   # Para codificar los enteros en binario
import sys      # Para leer los argumentos del programa

# Comprobar número correcto de argumentos
if len(sys.argv) != 4:
    print(f"Uso: {sys.argv[0]} <server_host:port> <n1> <n2>")
    sys.exit(1)

# Extraer dirección del servidor y los dos números
host, port = sys.argv[1].split(':')
port = int(port)
num1 = int(sys.argv[2])
num2 = int(sys.argv[3])

# Crear socket UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    print(f"Enviando al servidor {host}:{port} los números {num1} y {num2}")

    # Empaquetar los dos enteros en formato binario (big endian)
    data = struct.pack("!ii", num1, num2)

    # Enviar al servidor
    s.sendto(data, (host, port))

    # Esperar la respuesta del servidor
    data = s.recv(1024)

    # Desempaquetar el resultado (entero de 4 bytes)
    result = struct.unpack("!i", data)[0]

    # Mostrar resultado final
    print(f"Resultado recibido: {result}")
