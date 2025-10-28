// ------------------------------------------------------------
// Interfaz remota del servicio RMI.
// Define los métodos que pueden invocarse de forma remota
// desde un cliente RMI.
// ------------------------------------------------------------

import java.rmi.*;  // Importa las clases necesarias para RMI (Remote, RemoteException)

// Toda interfaz RMI debe:
/// 1. Extender la interfaz java.rmi.Remote
/// 2. Lanzar RemoteException en todos sus métodos

public interface Hello extends Remote {

    // Método remoto que puede ser invocado desde un cliente
    // Devuelve un String con un saludo.
    // RemoteException: se lanza si ocurre un problema en la comunicación.
    public String sayHello() throws RemoteException;
}
