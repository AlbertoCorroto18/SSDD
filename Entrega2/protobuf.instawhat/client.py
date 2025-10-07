#!/usr/bin/python3
# ------------------------------------------------------------
# CLIENTE INSTAWHAT
# ------------------------------------------------------------
# - Se conecta al servidor UDP indicado
# - Envía peticiones protobuf (Request)
# - Recibe y muestra respuestas protobuf (Response)
# - Soporta las operaciones definidas en el servidor
# ------------------------------------------------------------

import sys
import socket
import argparse
import instawhat_pb2 as instawhat  # type: ignore # Módulo generado por protoc

# Credenciales predefinidas (simulan autenticación)
CREDENTIALS = ['John.Doe', 'password']


# ------------------------------------------------------------
# Clase principal del cliente
# ------------------------------------------------------------
class InstaWhatClient:
    def __init__(self, host, port):
        # Crear socket UDP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (host, port)

    # --------------------------------------------------------
    # Enviar solicitud genérica y recibir respuesta
    # --------------------------------------------------------
    def handle_request(self, request, ResponseType=instawhat.Response):
        # Serializar mensaje protobuf y enviarlo
        self.sock.sendto(
            request.SerializeToString(),
            self.server_address
        )

        # Esperar respuesta (hasta 4096 bytes)
        data = self.sock.recv(4096)

        # Deserializar la respuesta
        response = ResponseType()
        response.ParseFromString(data)

        # Cerrar el socket tras cada operación
        self.sock.close()
        return response

    # --------------------------------------------------------
    # Métodos para cada operación
    # --------------------------------------------------------

    def post_photo(self, **kwargs):
        request = instawhat.Request()
        request.post_photo.credentials.extend(CREDENTIALS)
        request.post_photo.photo_url = kwargs['photo_url']
        return self.handle_request(request)

    def comment_photo(self, **kwargs):
        request = instawhat.Request()
        request.comment_photo.credentials.extend(CREDENTIALS)
        request.comment_photo.owner_id = kwargs['owner_id']
        request.comment_photo.photo_url = kwargs['photo_url']
        request.comment_photo.comment = kwargs['comment']
        return self.handle_request(request)

    def rate_photo(self, **kwargs):
        request = instawhat.Request()
        request.rate_photo.credentials.extend(CREDENTIALS)
        request.rate_photo.owner_id = kwargs['owner_id']
        request.rate_photo.photo_url = kwargs['photo_url']
        request.rate_photo.rating = kwargs['rating']
        return self.handle_request(request)

    def like_photo(self, **kwargs):
        request = instawhat.Request()
        request.like_photo.credentials.extend(CREDENTIALS)
        request.like_photo.photo_url = kwargs['photo_url']
        request.like_photo.owner_id = kwargs['owner_id']
        return self.handle_request(request)

    def delete_photo(self, **kwargs):
        request = instawhat.Request()
        request.delete_photo.credentials.extend(CREDENTIALS)
        request.delete_photo.photo_url = kwargs['photo_url']
        return self.handle_request(request)

    def get_last_photos(self, **kwargs):
        request = instawhat.Request()
        request.get_last_photos.user_id = kwargs['user_id']
        return self.handle_request(
            request, instawhat.GetLastPhotosResponse
        )


# ------------------------------------------------------------
# Programa principal
# ------------------------------------------------------------
def main():
    # Crear cliente con los parámetros introducidos
    client = InstaWhatClient(args.host, args.port)

    # Llamar dinámicamente al método según la operación
    response = getattr(client, args.operation)(**vars(args))

    # Comprobar si hubo error o éxito
    if response.HasField('error'):
        print('Error '
              + f'{instawhat.Error.ErrorCode.Name(response.error.code)}'
              + ': ' + response.error.message)
        sys.exit(1)

    print('Éxito:', response.success.message)

    # Si se pidió get_last_photos, mostrar lista
    if args.operation == 'get_last_photos':
        for photo_url in response.photo_urls:
            print(photo_url)


# ------------------------------------------------------------
# Configurar argparse para leer comandos por terminal
# ------------------------------------------------------------
parser = argparse.ArgumentParser(description="Cliente para InstaWhat")

parser.add_argument("host", help="Host del servidor")
parser.add_argument("port", type=int, help="Puerto del servidor")

# Subcomandos (uno por operación)
subparsers = parser.add_subparsers(dest="operation", help="Operaciones disponibles")

# POST PHOTO
post_photo_parser = subparsers.add_parser("post_photo", help="Publicar una foto")
post_photo_parser.add_argument("photo_url", help="URL de la foto")

# COMMENT PHOTO
comment_photo_parser = subparsers.add_parser("comment_photo", help="Comentar una foto")
comment_photo_parser.add_argument("owner_id", help="ID del propietario de la foto")
comment_photo_parser.add_argument("photo_url", help="URL de la foto")
comment_photo_parser.add_argument("comment", help="Comentario")

# RATE PHOTO
rate_photo_parser = subparsers.add_parser("rate_photo", help="Valorar una foto")
rate_photo_parser.add_argument("owner_id", help="ID del propietario")
rate_photo_parser.add_argument("photo_url", help="URL de la foto")
rate_photo_parser.add_argument("rating", type=int, help="Puntuación (entero)")

# LIKE PHOTO
like_photo_parser = subparsers.add_parser("like_photo", help="Dar 'like' a una foto")
like_photo_parser.add_argument("owner_id", help="ID del propietario")
like_photo_parser.add_argument("photo_url", help="URL de la foto")

# DELETE PHOTO
delete_photo_parser = subparsers.add_parser("delete_photo", help="Eliminar una foto")
delete_photo_parser.add_argument("photo_url", help="URL de la foto")

# GET LAST PHOTOS
get_last_photos_parser = subparsers.add_parser("get_last_photos", help="Ver las últimas fotos de un usuario")
get_last_photos_parser.add_argument("user_id", help="ID del usuario")

# Leer los argumentos
args = parser.parse_args()

# Ejecutar el cliente
main()
