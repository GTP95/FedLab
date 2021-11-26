package ml.gtpware;

import java.io.File;
import java.io.IOException;
import java.net.ServerSocket;

public class Main {
    private static int port;
    private static String iface;
    public static void main(String[] args){
        if(args.length!=2){
            System.out.println("Usage: sniff-capability.jar interfaceToSniff listenPort");
            return;
        }
        iface=args[0];
        port=Integer.parseInt(args[1]);
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

    public static String getIface(){
        return iface;
    }
}
