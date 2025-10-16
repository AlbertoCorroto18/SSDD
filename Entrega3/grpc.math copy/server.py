#!/usr/bin/env python3
# Servidor gRPC para operaciones matemáticas básicas (Add / Multiply).

from concurrent import futures
import grpc
import time

import math_pb2
import math_pb2_grpc


class MathService(math_pb2_grpc.MathServiceServicer):
    """Implementa las operaciones definidas en el servicio gRPC."""

    def Add(self, request, context):
        """Suma todos los números recibidos en la petición."""
        numbers = request.numbers
        print(f"[SERVER] Add({numbers})")
        result = sum(numbers)
        return math_pb2.Reply(result=result, operation="add")

    def Multiply(self, request, context):
        """Multiplica todos los números recibidos en la petición."""
        numbers = request.numbers
        print(f"[SERVER] Multiply({numbers})")
        result = 1
        for n in numbers:
            result *= n
        return math_pb2.Reply(result=result, operation="multiply")


def serve():
    """Inicia el servidor gRPC en el puerto 50051."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    math_pb2_grpc.add_MathServiceServicer_to_server(MathService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("🚀 Servidor Math gRPC ejecutándose en el puerto 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido.")
        server.stop(0)


if __name__ == "__main__":
    serve()
