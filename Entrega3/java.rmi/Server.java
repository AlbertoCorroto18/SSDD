// ------------------------------------------------------------
// Servidor RMI.
// Registra el objeto remoto en el RMI Registry para que los
// clientes puedan encontrarlo e invocar sus métodos.
// ------------------------------------------------------------

import java.rmi.*;             // API RMI general (Remote, Naming, etc.)
import java.rmi.server.*;      // Contiene UnicastRemoteObject (necesario para exportar el objeto remoto)

// Implementa la interfaz remota "Hello"
public class Server extends UnicastRemoteObject implements Hello {

    // Constructor obligatorio: debe lanzar RemoteException
    public Server() throws RemoteException {
        super();  // Llama al constructor de UnicastRemoteObject
    }

    // Implementación del método remoto definido en Hello.java
    @Override
    public String sayHello() throws RemoteException {
        // Devuelve el saludo cuando es invocado remotamente por un cliente
        return "Hello, world! (mensaje desde el servidor RMI)";
    }

    // Método main: inicia el servidor RMI
    public static void main(String args[]) {
        try {
            // Crea una instancia del objeto remoto
            Server obj = new Server();

            // Registra el objeto remoto con el nombre "Hello"
            // Esto hace que el cliente pueda buscarlo con el mismo nombre.
            Naming.rebind("Hello", obj);

            System.out.println("Servidor RMI listo y registrado como 'Hello'");

        } catch (Exception e) {
            // Captura cualquier error (p. ej. el registro RMI no iniciado)
            System.out.println("Error en el servidor RMI: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
