package ml.gtpware;

import java.io.*;
import java.net.Socket;

public class ConnectionHandler implements Runnable{
    private final Socket clientSocket;
    private final Status status;

    public ConnectionHandler(Socket clientSocket) {
        this.clientSocket=clientSocket;
        this.status=Status.getInstance();
    }

    @Override
    public void run() {
        try {
            BufferedReader in= new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
            out.println("Welcome! To start a new packet capture, send \"capture\" without quotes. To stop a capture, send \"stop $TOKEN\" without quotes, where $TOKEN is the token you received when you started the capture");
            String command=in.readLine();
            PacketCaptureDetails packetCaptureDetails;
            if(command.equals("capture")){
                packetCaptureDetails=status.requestPacketCapture();
                if(packetCaptureDetails.granted){
                    out.println("Your packet capture has been started. To later stop it, use the following token: "+packetCaptureDetails.token);
                    out.println("You packet capture will be saved as "+packetCaptureDetails.fileName);
                }
                else{
                    out.println("There is already a packet capture in progress. " +
                            "To avoid mixing you experiment's results with someone else's experiment, " +
                            "it is not possible to start another one at the moment. Please try again later");
                }
            }
            if(command.startsWith("stop")){
                String[] elements=command.split(" ", 2);
                if(status.stopPacketCapture(elements[1])){
                    out.println("Packet capture completed, you can now download the result");
                }
                else{
                    out.println("Couldn't stop packet capture: either wrong token or no capture is in progress");
                }
            }
            else out.println("Sorry, couldn't understand your command");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
