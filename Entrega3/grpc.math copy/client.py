#!/usr/bin/env python3
# ------------------------------------------------------------
# Cliente gRPC para el servicio Math.
# Permite conectarse a un servidor remoto y realizar operaciones
# de suma o multiplicación sobre una lista de números.
# ------------------------------------------------------------

# Muestra un mensaje de uso si no se proporcionan argumentos correctos
"Usage: {0} <server_host:port> {add|mul} <n1> <n2> [n3 ...]"

import sys
import grpc

# Módulos generados por el compilador de gRPC
import math_pb2
import math_pb2_grpc


# ------------------------------------------------------------
# Validación de los argumentos de entrada
# ------------------------------------------------------------
# Debe recibir al menos:
#  argv[1] = servidor (host:port)
#  argv[2] = operación ("add" o "mul")
#  argv[3..] = lista de números enteros
if len(sys.argv) < 2:
    print(__doc__.format(sys.argv[0]))  # Muestra la ayuda
    sys.exit(1)

# Extrae los valores de la línea de comandos
server = sys.argv[1]
operation = sys.argv[2]
# Convierte el resto de argumentos a enteros (list comprehension)
numbers = [int(x) for x in sys.argv[3:]]

# ------------------------------------------------------------
# Creación del canal y stub del servicio
# ------------------------------------------------------------
# Abre un canal inseguro hacia el servidor (por ejemplo "localhost:10001")
channel = grpc.insecure_channel(server)

# Crea un cliente (stub) del servicio Math, usando el canal anterior
stub = math_pb2_grpc.MathStub(channel)

# ------------------------------------------------------------
# Construcción del mensaje de solicitud (Request)
# ------------------------------------------------------------
# El mensaje Request tiene un campo "repeated int32 numbers"
# En Python se pasa una lista de enteros.
request = math_pb2.Request(numbers=numbers)

# ------------------------------------------------------------
# Ejecución remota del método RPC correspondiente
# ------------------------------------------------------------
# Dependiendo del argumento, llama al método remoto add o multiply.
# "stub.add" y "stub.multiply" son métodos que gRPC generó automáticamente.
calc = stub.add if operation == 'add' else stub.multiply

# Llama al método remoto pasando el mensaje de solicitud
response = calc(request)

# ------------------------------------------------------------
# Muestra el resultado en consola
# ------------------------------------------------------------
print(f'Result: {response.result}')
