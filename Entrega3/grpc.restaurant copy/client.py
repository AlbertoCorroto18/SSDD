#!/usr/bin/env python3
# Cliente gRPC de ejemplo para el sistema de reservas.
# Demuestra crear, consultar, listar y cancelar reservas.

import sys
import grpc

import app_pb2
import app_pb2_grpc


def run(host: str = "localhost:50051"):
    # Crea canal y stub del servicio
    with grpc.insecure_channel(host) as channel:
        stub = app_pb2_grpc.RestaurantServiceStub(channel)

        # 1) Crear una reserva
        name = "Alice"
        size = 2
        when = "2025-10-16T20:30"
        if len(sys.argv) >= 4:
            name, size, when = sys.argv[1], int(sys.argv[2]), sys.argv[3]

        print(f"[MakeReservation] name={name}, party_size={size}, datetime={when}")
        make_res = stub.MakeReservation(app_pb2.MakeReservationRequest(
            customer_name=name,
            party_size=size,
            datetime_iso=when
        ))
        print("→ reply:", make_res)

        if make_res.status != "CONFIRMED":
            print("Reservation rejected:", make_res.message)
            return

        res_id = make_res.reservation_id

        # 2) Consultar la reserva creada
        print(f"\n[GetReservation] id={res_id}")
        get_res = stub.GetReservation(app_pb2.GetReservationRequest(reservation_id=res_id))
        print("→ reply:", get_res)

        # 3) Listar reservas (todas)
        print("\n[ListReservations] all")
        list_all = stub.ListReservations(app_pb2.ListReservationsRequest())
        for r in list_all.reservations:
            print(f"  - {r.reservation_id} | {r.customer_name} | {r.party_size} | {r.datetime_iso} | {r.status}")

        # 4) Listar reservas por fecha (YYYY-MM-DD)
        date = when[:10]
        print(f"\n[ListReservations] date={date}")
        list_day = stub.ListReservations(app_pb2.ListReservationsRequest(date_iso=date))
        for r in list_day.reservations:
            print(f"  - {r.reservation_id} | {r.customer_name} | {r.party_size} | {r.datetime_iso} | {r.status}")

        # 5) Cancelar la reserva
        print(f"\n[CancelReservation] id={res_id}")
        cancel_res = stub.CancelReservation(app_pb2.CancelReservationRequest(reservation_id=res_id))
        print("→ reply:", cancel_res)

        # 6) Volver a consultar para ver el estado CANCELLED
        print(f"\n[GetReservation] id={res_id} (after cancel)")
        get_res2 = stub.GetReservation(app_pb2.GetReservationRequest(reservation_id=res_id))
        print("→ reply:", get_res2)


if __name__ == "__main__":
    # Permite pasar host por argv[4] opcionalmente
    # Ej: python client.py Bob 4 2025-12-31T22:00 localhost:50051
    host = "localhost:50051"
    if len(sys.argv) >= 5:
        host = sys.argv[4]
    run(host)
