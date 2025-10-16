#!/usr/bin/env python3
# Cliente gRPC para probar el servicio MathService (Add / Multiply).

import grpc
import sys
import math_pb2
import math_pb2_grpc


def run():
    # Permite pasar los números por argumentos, si no se usan, aplica por defecto
    numbers = [1, 2, 3, 4, 5]
    if len(sys.argv) > 1:
        numbers = [int(x) for x in sys.argv[1:]]

    # Crea canal y stub
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = math_pb2_grpc.MathServiceStub(channel)

        print(f"[CLIENT] Enviando números: {numbers}")

        # Llamada RPC para suma
        add_response = stub.Add(math_pb2.Request(numbers=numbers))
        print(f"🧮 Resultado de Add: {add_response.result}")

        # Llamada RPC para multiplicación
        multiply_response = stub.Multiply(math_pb2.Request(numbers=numbers))
        print(f"✖️ Resultado de Multiply: {multiply_response.result}")


if __name__ == "__main__":
    run()
