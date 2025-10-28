#!/usr/bin/env python3
# Ejemplo basado en https://github.com/grpc/grpc/tree/v1.6.x/examples/python/helloworld
# ------------------------------------------------------------
# Este script implementa un servidor gRPC que expone el servicio "Hello"
# definido en hello.proto. El servidor escucha peticiones del cliente y
# muestra el mensaje recibido por consola.
# ------------------------------------------------------------

from concurrent import futures  # Permite manejar múltiples peticiones RPC concurrentes
import grpc                      # Librería principal de gRPC
import hello_pb2                 # Módulo generado a partir del .proto (mensajes)
import hello_pb2_grpc            # Módulo generado a partir del .proto (servicio y stub)


# ------------------------------------------------------------
# Clase que implementa el servicio remoto Hello
# ------------------------------------------------------------
class Hello(hello_pb2_grpc.HelloServicer):  # Hereda del servicio generado por gRPC
    def write(self, request, context):
        # Muestra por consola el mensaje recibido desde el cliente
        print("Client sent: '{}'".format(request.message))
        # Devuelve una respuesta vacía (PrintReply no tiene campos)
        return hello_pb2.PrintReply()


# ------------------------------------------------------------
# Configuración y arranque del servidor gRPC
# ------------------------------------------------------------
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
# Registra la implementación de Hello en el servidor
hello_pb2_grpc.add_HelloServicer_to_server(Hello(), server)
# Escucha en todas las interfaces, puerto 2000
server.add_insecure_port('0.0.0.0:2000')
# Inicia el servidor
server.start()

try:
    # Mantiene el servidor activo hasta interrupción manual
    server.wait_for_termination()
except KeyboardInterrupt:
    # Detiene el servidor limpiamente al presionar Ctrl+C
    server.stop(0)
