import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;

// Implementa la interfaz remota
public class Server implements Hello {

    // Implementación del método remoto
    public String sayHello() {
        return "Hello, world!";
    }

    public static void main(String args[]) {
        try {
            // Crea una instancia del servidor (objeto remoto)
            Server obj = new Server();

            // Exporta el objeto para que pueda ser accedido remotamente
            Hello stub = (Hello) UnicastRemoteObject.exportObject(obj, 0);

            // Crea el registro RMI (binder) en el puerto 1099
            Registry registry = LocateRegistry.createRegistry(1099);

            // Asocia el nombre "Hello" al objeto remoto
            registry.rebind("Hello", stub);

            System.out.println("Server ready");
        } catch (Exception e) {
            System.err.println("Server exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
