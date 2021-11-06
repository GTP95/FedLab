/**
 * Quick and dirty implementation of a server serving the file "device_directory" on port 1024
 * and reloading it when it gets modified
 */


package ml.gtpware;

import java.io.IOException;
import java.net.ServerSocket;

public class Main {
    private static final int port=1024;
    private static FileReader fileReader;

    public static void main(String[] args) {
        fileReader=FileReader.getInstance();
        ModificationListener modificationListener=new ModificationListener(fileReader);
        new Thread(modificationListener).start();
        try {
            ServerSocket serverSocket=new ServerSocket(port);
            while (true){
                ConnectionHandler connectionHandler=new ConnectionHandler(serverSocket.accept());
                new Thread(connectionHandler).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }


    }



    }



