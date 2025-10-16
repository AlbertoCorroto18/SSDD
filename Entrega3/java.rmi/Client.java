import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class Client {
    private Client() {}

    public static void main(String[] args) {
        try {
            // Localiza el registro RMI (binder) en localhost
            Registry registry = LocateRegistry.getRegistry(null);

            // Obtiene la referencia remota al objeto "Hello"
            Hello stub = (Hello) registry.lookup("Hello");

            // Llama al método remoto y muestra el resultado
            String response = stub.sayHello();
            System.out.println("response: " + response);

        } catch (Exception e) {
            System.err.println("Client exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
