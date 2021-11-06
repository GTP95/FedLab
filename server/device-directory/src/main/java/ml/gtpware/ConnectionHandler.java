package ml.gtpware;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

public class ConnectionHandler implements Runnable{
    private Socket clientSocket;

    public ConnectionHandler(Socket clientSocket) {
        this.clientSocket=clientSocket;
    }

    @Override
    public void run() {
        try {
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
            out.println(FileReader.getInstance().readFile()); //Sends the content of the device directory
            out.close();    //terminate connection
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
