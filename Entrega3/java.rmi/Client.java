// ------------------------------------------------------------
// Cliente RMI.
// Busca el objeto remoto registrado y ejecuta su método "sayHello".
// ------------------------------------------------------------

import java.rmi.*;  // Para Naming.lookup y manejo de excepciones RMI

public class Client {
    public static void main(String args[]) {
        try {
            // Busca el objeto remoto en el registro RMI usando el nombre "Hello"
            // El prefijo "rmi://localhost/Hello" indica que se conecta al registro
            // local (puerto 1099 por defecto)
            Hello obj = (Hello) Naming.lookup("rmi://localhost/Hello");

            // Invoca el método remoto 'sayHello' (ejecutado en el servidor)
            String message = obj.sayHello();

            // Muestra la respuesta devuelta por el servidor
            System.out.println("Respuesta del servidor: " + message);

        } catch (Exception e) {
            // Manejo de errores de red o registro
            System.out.println("Error en el cliente RMI: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
