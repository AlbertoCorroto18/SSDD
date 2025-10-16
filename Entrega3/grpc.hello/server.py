import grpc
from concurrent import futures
import time
import hello_pb2
import hello_pb2_grpc

# Clase que implementa el servicio definido en hello.proto
class HelloServicer(hello_pb2_grpc.HelloServicer):

    # Implementación del método remoto "write"
    def write(self, request, context):
        print(f"Cliente envió: {request.message}")   # Muestra el mensaje recibido
        return hello_pb2.PrintReply()                 # Devuelve respuesta vacía

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # Servidor multihilo
    hello_pb2_grpc.add_HelloServicer_to_server(HelloServicer(), server)
    server.add_insecure_port('[::]:50051')            # Escucha en el puerto 50051
    server.start()
    print("Servidor gRPC activo en el puerto 50051")
    try:
        while True:
            time.sleep(86400)  # Mantiene el servidor corriendo
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
