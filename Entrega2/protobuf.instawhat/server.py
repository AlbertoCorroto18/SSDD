#!/usr/bin/python3
# ------------------------------------------------------------
# SERVIDOR INSTAWHAT
# ------------------------------------------------------------
# - Usa UDP (no hay conexión persistente)
# - Recibe peticiones en formato Protocol Buffers (protobuf)
# - Soporta operaciones: post_photo, comment_photo, rate_photo,
#   like_photo, delete_photo y get_last_photos
# - Devuelve un mensaje de respuesta también en protobuf
# ------------------------------------------------------------

import sys
import socket
import instawhat_pb2 as instawhat  # type: ignore # Módulo generado por protoc

# El puerto se pasa como argumento al ejecutar
SOCKET_PORT = int(sys.argv[1])

# ------------------------------------------------------------
# Clase User: representa a un usuario del sistema
# ------------------------------------------------------------
class User:
    def __init__(self, user_id, user_password):
        self.id = user_id
        self.password = user_password
        self.photos = []  # lista de URLs publicadas por el usuario

# ------------------------------------------------------------
# Clase Server: gestiona los usuarios y las peticiones
# ------------------------------------------------------------
class Server:
    def __init__(self):
        # Usuarios predefinidos con contraseña
        self.users = {
            'John.Doe': User('John.Doe', 'password'),
            'Jane.Doe': User('Jane.Doe', 'password')
        }

        # Crear socket UDP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Asociarlo a todas las interfaces y al puerto
        self.sock.bind(('', SOCKET_PORT))
        print(f'Servidor escuchando en el puerto {SOCKET_PORT}')

    # --------------------------------------------------------
    # Bucle principal: el servidor nunca se detiene
    # --------------------------------------------------------
    def run(self):
        while True:
            # Esperar mensajes del cliente
            data, client = self.sock.recvfrom(4096)
            request = instawhat.Request()
            request.ParseFromString(data)  # Deserializar mensaje
            print(f'Request recibido de {client}')

            # Obtener el tipo de operación pedida (oneof)
            operation = self.get_operation_handler(request)

            # Ejecutar la operación correspondiente
            if operation:
                response = operation(request)
            else:
                response = instawhat.Response()
                response.error.code = instawhat.Error.INVALID_DATA
                response.error.message = 'Operación no válida'

            # Enviar la respuesta serializada al cliente
            self.sock.sendto(response.SerializeToString(), client)

    # --------------------------------------------------------
    # Determina qué tipo de petición ha llegado
    # --------------------------------------------------------
    def get_operation_handler(self, request):
        operation_type = request.WhichOneof('request')
        return getattr(self, operation_type.lower(), None)

    # --------------------------------------------------------
    # Operaciones soportadas
    # --------------------------------------------------------

    def post_photo(self, request):
        """Publicar una foto."""
        user = self.users[request.post_photo.credentials[0]]
        response = instawhat.Response()

        # Verificar existencia de usuario
        if not user:
            response.error.code = instawhat.Error.NOT_FOUND
            response.error.message = 'Usuario no encontrado'
            return response

        # Verificar contraseña
        if user.password != request.post_photo.credentials[1]:
            response.error.code = instawhat.Error.UNAUTHORIZED
            response.error.message = 'Contraseña incorrecta'
            return response

        # Verificar si la foto ya estaba publicada
        if request.post_photo.photo_url in user.photos:
            response.error.code = instawhat.Error.ALREADY_EXISTS
            response.error.message = 'La foto ya fue publicada'
            return response

        # Guardar la nueva foto
        user.photos.append(request.post_photo.photo_url)
        response.success.message = 'Foto publicada correctamente'
        print(f'Foto publicada: {request.post_photo.photo_url}')
        return response

    def comment_photo(self, request):
        """Comentar una foto (simulado)."""
        print(f'Comentario en {request.comment_photo.photo_url}:')
        print(f'"{request.comment_photo.comment}"')
        response = instawhat.Response()
        response.success.message = 'Comentario publicado'
        return response

    def rate_photo(self, request):
        """Valorar una foto (simulado)."""
        print(f'Valoración {request.rate_photo.photo_url}: '
              f'{request.rate_photo.rating}')
        response = instawhat.Response()
        response.success.message = 'Foto valorada'
        return response

    def like_photo(self, request):
        """Dar like (simulado)."""
        print(f'Like en foto {request.like_photo.photo_url}')
        response = instawhat.Response()
        response.success.message = 'Like registrado'
        return response

    def delete_photo(self, request):
        """Borrar una foto (simulado)."""
        print(f'Eliminar foto {request.delete_photo.photo_url}')
        response = instawhat.Response()
        response.success.message = 'Foto eliminada'
        return response

    def get_last_photos(self, request):
        """Obtener últimas fotos publicadas (simulado)."""
        print(f'Fotos del usuario {request.get_last_photos.user_id}')
        response = instawhat.GetLastPhotosResponse()
        response.photo_urls.extend(['photo1', 'photo2', 'photo3'])
        response.success.message = 'Fotos recuperadas'
        return response


# ------------------------------------------------------------
# Punto de entrada
# ------------------------------------------------------------
if __name__ == '__main__':
    server = Server()
    server.run()
