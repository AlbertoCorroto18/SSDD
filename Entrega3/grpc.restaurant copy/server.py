#!/usr/bin/env python3
# ------------------------------------------------------------
# Servidor gRPC para gestionar reservas de restaurante.
# Expone varios métodos RPC:
#   - makeReservation: crea una reserva nueva
#   - checkReservation: consulta una reserva existente
#   - cancelReservation: elimina una reserva por ID
#   - listReservations: muestra todas las reservas almacenadas
# ------------------------------------------------------------

import random                         # Para generar IDs aleatorios de reserva
import grpc                           # Librería principal gRPC
from concurrent import futures         # Para concurrencia en el servidor
from google.protobuf import empty_pb2  # Tipo vacío estándar de Google Protobuf

# Módulos generados por grpc_tools a partir de app.proto
import app_pb2
import app_pb2_grpc


# ------------------------------------------------------------
# Clase que implementa el servicio gRPC definido en app.proto
# ------------------------------------------------------------
class ReservationsService(app_pb2_grpc.ReservationsServicer):
    """
    Implementación de los métodos definidos en el servicio 'Reservations'
    (ver app.proto). Mantiene las reservas en un diccionario en memoria:
    { id_reserva : objeto Reservation }
    """

    def __init__(self):
        # Diccionario que almacena todas las reservas (simula una BD)
        self.reservations = {}

    # --------------------------------------------------------
    # Métodos auxiliares privados
    # --------------------------------------------------------

    def _get_or_404(self, id, context):
        """
        Comprueba si existe la reserva con el ID dado.
        Si no existe, aborta la RPC con código NOT_FOUND.
        """
        if not id:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                'Missing reservation ID'
            )

        if id not in self.reservations:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                'Reservation not found'
            )

    def _validate_new_reservation(self, req, context):
        """
        Valida los datos de una nueva reserva.
        Si falta algún campo obligatorio o hay valores inválidos,
        se aborta la llamada con código INVALID_ARGUMENT.
        """
        missing = []
        # Comprueba campos obligatorios (según el .proto)
        if not req.HasField("time"):  missing.append("time")
        if req.number_of_diners <= 0: missing.append("number_of_diners")
        if not req.client_name:       missing.append("client_name")
        if not req.contact_phone:     missing.append("contact_phone")

        # Si hay errores, cancela la llamada RPC con un mensaje de error
        if missing:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                f"Missing or invalid fields: {', '.join(missing)}"
            )

    # --------------------------------------------------------
    # Métodos RPC implementados (definidos en app.proto)
    # --------------------------------------------------------

    def makeReservation(self, request, context):
        """
        Crea una nueva reserva, valida los campos y la almacena en memoria.
        """
        # Verifica que los campos sean válidos
        self._validate_new_reservation(request, context)

        # Crea un objeto Reservation con los datos recibidos
        reservation = app_pb2.Reservation(
            id = random.randint(10000, 99999),  # ID único aleatorio
            time = request.time,
            number_of_diners = request.number_of_diners,
            client_name = request.client_name,
            contact_phone = request.contact_phone
        )

        # Guarda la reserva en el "diccionario de base de datos"
        self.reservations[reservation.id] = reservation

        # Muestra por consola (solo informativo)
        print(f'{context.peer()} :: Make {reservation.id}')

        # Devuelve la reserva completa (incluyendo el ID generado)
        return reservation


    def checkReservation(self, request, context):
        """
        Busca una reserva por ID y la devuelve.
        """
        self._get_or_404(request.id, context)  # Lanza error si no existe
        print(f'{context.peer()} :: Check {request.id}')
        return self.reservations[request.id]


    def cancelReservation(self, request, context):
        """
        Cancela (elimina) una reserva existente.
        """
        self._get_or_404(request.id, context)
        del self.reservations[request.id]   # Borra del diccionario
        print(f'{context.peer()} :: Cancel {request.id}')
        # Devuelve un mensaje vacío (Empty) como confirmación
        return empty_pb2.Empty()


    def listReservations(self, _, context):
        """
        Devuelve una lista de todas las reservas almacenadas.
        """
        print(f'{context.peer()} :: List')
        return app_pb2.ReservationsList(
            reservations = list(self.reservations.values())
        )


# ------------------------------------------------------------
# Arranque del servidor gRPC
# ------------------------------------------------------------
print("Bootstrapping gRPC server...")

# Crea el servidor gRPC con hasta 10 hilos simultáneos
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# Registra la implementación del servicio Reservations
app_pb2_grpc.add_ReservationsServicer_to_server(ReservationsService(), server)

# Asigna el puerto 10001 (escucha IPv4 e IPv6)
server.add_insecure_port('[::]:10001')

# Inicia el servidor
server.start()
print(f'Server started...')

# Mantiene el servidor activo hasta interrupción manual
try:
    server.wait_for_termination()
except KeyboardInterrupt:
    print("Stopping server...")
    server.stop(0)
