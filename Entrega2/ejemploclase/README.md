        CLIENTE (Sensor)                     SERVIDOR
    ┌────────────────────┐            ┌────────────────────────┐
    | sensor.proto       |            | sensor.proto           |
    | sensor_pb2.Reading |            | sensor_pb2.Reading     |
    └────────────────────┘            └────────────────────────┘
                │                                 │
                │  SerializeToString()            │
                │──────────────► (UDP, port 1234) │
                │                                 │
                │                                 │ ParseFromString()
                │                                 ▼
                │                     Mostrar lectura decodificada
                │                                 │
                │───────────────(loop forever)────│



##Cómo ejecutar el sistema
Compilar el .proto (solo una vez)
protoc --python_out=. sensor.proto


Esto genera sensor_pb2.py.

##Ejecutar el servidor
python3 udp-server.py

##Ejecutar el cliente
python3 udp-client.py localhost


##Salida esperada:

Sensor conectado: ('127.0.0.1', 57890)
Datos crudos:
b'\n\x01\x01\x10\x01\x1d\xcd\xccL>\x22\x05kg/m3'
Sensor 1 (HUMIDITY) valor: 0.20 kg/m3