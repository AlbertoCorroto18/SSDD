#!/usr/bin/env python3
# ------------------------------------------------------------
# Servidor gRPC para operaciones matemáticas básicas.
# Expone dos métodos remotos:
#   - add: suma una lista de números
#   - multiply: multiplica una lista de números
# ------------------------------------------------------------

# Importa la librería principal de gRPC en Python
import grpc
# Permite la ejecución concurrente de peticiones RPC
from concurrent import futures

# Importa los módulos generados por el compilador de gRPC
# a partir del archivo math.proto.
import math_pb2
import math_pb2_grpc


# ------------------------------------------------------------
# Implementación del servicio definido en math.proto
# ------------------------------------------------------------
class MathService(math_pb2_grpc.MathServicer):
    """
    Clase que implementa los métodos RPC declarados en el servicio Math
    dentro del archivo math.proto.

    Cada método recibe:
    - request: objeto del tipo definido en el .proto (Request)
    - context: información de contexto de la llamada RPC (para códigos de error, metadatos, etc.)
    """

    # Método RPC 'add' → suma todos los números recibidos
    def add(self, request, context):
        # request.numbers es una lista (repeated int32 en .proto)
        result = sum(request.numbers)
        # Devuelve una instancia del mensaje Response con el resultado
        return math_pb2.Response(result=result)

    # Método RPC 'multiply' → multiplica todos los números de la lista
    def multiply(self, request, context):
        # Inicializa el resultado en 1 (elemento neutro de la multiplicación)
        result = 1
        # Recorre todos los valores recibidos y los multiplica
        for n in request.numbers:
            result *= n
        # Devuelve un mensaje Response con el producto total
        return math_pb2.Response(result=result)


# ------------------------------------------------------------
# Configuración y arranque del servidor gRPC
# ------------------------------------------------------------

# Crea un servidor gRPC con un pool de hilos (máx. 10 hilos)
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# Registra la implementación del servicio Math en el servidor
math_pb2_grpc.add_MathServicer_to_server(MathService(), server)

# Asigna el puerto 10001 (en todas las interfaces IPv4 e IPv6)
server.add_insecure_port('[::]:10001')

# Inicia el servidor (empieza a escuchar peticiones)
server.start()

try:
    print("\nWaiting for a request...")  # Mensaje informativo en consola
    # Mantiene el servidor activo hasta interrupción manual
    server.wait_for_termination()

# Permite detener el servidor limpiamente con Ctrl+C
except KeyboardInterrupt:
    server.stop(0)
