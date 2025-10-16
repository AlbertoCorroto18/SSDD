import java.rmi.Remote;           // Interfaz base para objetos remotos
import java.rmi.RemoteException;  // Excepción obligatoria en métodos remotos

// La interfaz define los métodos que pueden llamarse remotamente
public interface Hello extends Remote {
    String sayHello() throws RemoteException;   // Método remoto
}
