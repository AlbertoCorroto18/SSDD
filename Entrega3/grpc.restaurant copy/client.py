#!/usr/bin/env python3
# ------------------------------------------------------------
# Cliente gRPC para el sistema de reservas.
# Permite crear, consultar, eliminar y listar reservas usando
# subcomandos de línea de comandos (argparse).
# ------------------------------------------------------------

import sys
import random
import argparse
import grpc
from datetime import datetime, timezone
from google.protobuf import empty_pb2

# Módulos generados
import app_pb2
import app_pb2_grpc


# ------------------------------------------------------------
# Clase que encapsula las llamadas RPC al servidor
# ------------------------------------------------------------
class ReservationClient:
    def __init__(self, stub):
        # El stub es el proxy gRPC del servicio remoto
        self.stub = stub

    def call_remote(self, func, request):
        """
        Función auxiliar para ejecutar un método remoto
        y capturar los posibles errores de red o validación.
        """
        try:
            response = func(request)
        except grpc.RpcError as e:
            print(f'Error: {e.code().name} - {e.details()}')
            sys.exit(1)
        return response

    # --------------------------------------------------------
    # Métodos cliente → equivalentes a las operaciones del servicio
    # --------------------------------------------------------

    def makeReservation(self):
        """
        Crea una reserva nueva con datos aleatorios de ejemplo.
        """
        request = app_pb2.NewReservationRequest(
            number_of_diners = random.randint(1, 10),
            client_name = 'John Doe',
            contact_phone = '555-555-555'
        )
        # Asigna la hora actual como timestamp
        request.time.FromDatetime(datetime.now(tz=timezone.utc))

        # Llama al servidor para crear la reserva
        try:
            response = self.stub.makeReservation(request)
        except grpc.RpcError as e:
            print(f'Error: {e.code().name} - {e.details()}')
            sys.exit(1)

        print(response)  # Muestra la reserva devuelta (con ID asignado)

    def checkReservation(self, id):
        """
        Consulta una reserva concreta por ID.
        """
        try:
            response = self.stub.checkReservation(
                app_pb2.ReservationIdRequest(id=int(id))
            )
        except grpc.RpcError as e:
            print(f'Error: {e.code().name} - {e.details()}')
            sys.exit(1)
        print(response)

    def cancelReservation(self, id):
        """
        Cancela una reserva (la elimina del servidor).
        """
        try:
            response = self.stub.cancelReservation(
                app_pb2.ReservationIdRequest(id=int(id))
            )
        except grpc.RpcError as e:
            print(f'Error: {e.code().name} - {e.details()}')
            sys.exit(1)
        print('Reservation cancelled')

    def listReservations(self):
        """
        Muestra todas las reservas activas en el servidor.
        """
        response = self.stub.listReservations(empty_pb2.Empty())
        for reservation in response.reservations:
            print(reservation)


# ------------------------------------------------------------
# Argumentos de línea de comandos (modo consola)
# ------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('server', type=str, help="Dirección del servidor gRPC (host:port)")
parser.add_argument('-m', '--make', action='store_true', help="Crear reserva nueva")
parser.add_argument('-c', '--check', type=str, help="Consultar reserva por ID")
parser.add_argument('-r', '--remove', type=str, help="Cancelar reserva por ID")
parser.add_argument('-l', '--list', action='store_true', help="Listar todas las reservas")
args = parser.parse_args()

# ------------------------------------------------------------
# Creación del canal y stub
# ------------------------------------------------------------
channel = grpc.insecure_channel(args.server)
stub = app_pb2_grpc.ReservationsStub(channel)
client = ReservationClient(stub)

# ------------------------------------------------------------
# Lógica principal: elige la operación según el argumento
# ------------------------------------------------------------
if args.make:
    client.makeReservation()
elif args.check:
    client.checkReservation(args.check)
elif args.remove:
    client.cancelReservation(args.remove)
else:
    client.listReservations()
