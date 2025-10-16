import grpc
import hello_pb2
import hello_pb2_grpc
import sys

def run():
    with grpc.insecure_channel('localhost:50051') as channel:   # Crea canal hacia el servidor
        stub = hello_pb2_grpc.HelloStub(channel)                # Crea el stub del servicio
        message = "Hola desde el cliente!"
        if len(sys.argv) > 1:
            message = sys.argv[1]
        request = hello_pb2.PrintRequest(message=message)        # Construye mensaje de solicitud
        response = stub.write(request)                           # Llama remotamente al método "write"
        print("Mensaje enviado al servidor:", message)

if __name__ == '__main__':
    run()
