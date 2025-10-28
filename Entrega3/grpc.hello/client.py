#!/usr/bin/env python3
# Ejemplo basado en https://github.com/grpc/grpc/tree/v1.6.x/examples/python/helloworld
# ------------------------------------------------------------
# Este script implementa el cliente gRPC que se conecta al servidor Hello.
# Envía un mensaje de texto mediante el método remoto "write".
# ------------------------------------------------------------

import sys          # Para leer los argumentos de línea de comandos
import grpc         # Librería principal de gRPC
import hello_pb2    # Mensajes generados desde el archivo .proto
import hello_pb2_grpc  # Clases del servicio y stub generadas desde el .proto


# ------------------------------------------------------------
# Comprobación de argumentos: se espera <server> <port>
# ------------------------------------------------------------
if len(sys.argv) != 3:
    print("usage: ./client.py <server> <port>")
    sys.exit(1)

server = sys.argv[1]  # Dirección IP o hostname del servidor
port = sys.argv[2]    # Puerto donde escucha el servidor

# ------------------------------------------------------------
# Creación del canal gRPC
# ------------------------------------------------------------
# Crea un canal inseguro (sin TLS) para conectarse al servidor
channel = grpc.insecure_channel(f'{server}:{port}')

# Crea un stub (proxy) del servicio remoto Hello
stub = hello_pb2_grpc.HelloStub(channel)

# Crea el mensaje que se enviará al servidor (PrintRequest)
message = hello_pb2.PrintRequest(message='hello')

# Llama al método remoto 'write' definido en el servidor
stub.write(message)
# (El servidor imprimirá el mensaje recibido; este cliente no espera respuesta con contenido)
