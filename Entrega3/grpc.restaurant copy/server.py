#!/usr/bin/env python3
# Servidor gRPC para un sistema simple de reservas de restaurante.
# Mantiene reservas en memoria (diccionario) para la demo.

import time
import uuid
from concurrent import futures

import grpc

import app_pb2
import app_pb2_grpc


class ReservationStore:
    """Almacén en memoria de reservas (demo)."""
    def __init__(self):
        self._data = {}  # reservation_id -> dict

    def create(self, customer_name: str, party_size: int, datetime_iso: str):
        # Aquí podrías verificar disponibilidad, solapes, aforo, etc.
        reservation_id = str(uuid.uuid4())[:8]
        record = {
            "reservation_id": reservation_id,
            "customer_name": customer_name,
            "party_size": party_size,
            "datetime_iso": datetime_iso,
            "status": "CONFIRMED",
        }
        self._data[reservation_id] = record
        return record

    def get(self, reservation_id: str):
        return self._data.get(reservation_id)

    def cancel(self, reservation_id: str):
        rec = self._data.get(reservation_id)
        if not rec:
            return False, "Reservation not found"
        if rec["status"] == "CANCELLED":
            return False, "Reservation already cancelled"
        rec["status"] = "CANCELLED"
        return True, "Reservation cancelled"

    def list_all(self, date_iso: str | None = None):
        if not date_iso:
            return list(self._data.values())
        # Filtra por fecha "YYYY-MM-DD" al inicio de datetime_iso
        return [r for r in self._data.values() if r["datetime_iso"].startswith(date_iso)]


class RestaurantService(app_pb2_grpc.RestaurantServiceServicer):
    def __init__(self, store: ReservationStore):
        self.store = store

    def MakeReservation(self, request, context):
        # request: MakeReservationRequest
        if not request.customer_name or request.party_size == 0 or not request.datetime_iso:
            return app_pb2.MakeReservationReply(
                reservation_id="",
                status="REJECTED",
                message="Missing required fields (customer_name, party_size, datetime_iso).",
            )
        rec = self.store.create(request.customer_name, request.party_size, request.datetime_iso)
        return app_pb2.MakeReservationReply(
            reservation_id=rec["reservation_id"],
            status=rec["status"],
            message=f"Reservation created for {rec['customer_name']} at {rec['datetime_iso']}",
        )

    def GetReservation(self, request, context):
        rec = self.store.get(request.reservation_id)
        if not rec:
            return app_pb2.GetReservationReply(found=False, message="Reservation not found")
        return app_pb2.GetReservationReply(
            found=True,
            data=app_pb2.Reservation(
                reservation_id=rec["reservation_id"],
                customer_name=rec["customer_name"],
                party_size=rec["party_size"],
                datetime_iso=rec["datetime_iso"],
                status=rec["status"],
            ),
            message="OK",
        )

    def CancelReservation(self, request, context):
        ok, msg = self.store.cancel(request.reservation_id)
        return app_pb2.CancelReservationReply(success=ok, message=msg)

    def ListReservations(self, request, context):
        items = self.store.list_all(request.date_iso or "")
        return app_pb2.ListReservationsReply(
            reservations=[
                app_pb2.Reservation(
                    reservation_id=r["reservation_id"],
                    customer_name=r["customer_name"],
                    party_size=r["party_size"],
                    datetime_iso=r["datetime_iso"],
                    status=r["status"],
                )
                for r in items
            ]
        )


def serve(host: str = "[::]:50051"):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store = ReservationStore()
    app_pb2_grpc.add_RestaurantServiceServicer_to_server(RestaurantService(store), server)
    server.add_insecure_port(host)
    server.start()
    print(f"Restaurant gRPC server listening on {host}")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("Stopping server...")
        server.stop(0)


if __name__ == "__main__":
    serve()
