package ml.gtpware;

public class PacketCaptureDetails {
    boolean granted;
    String token;
    String fileName;

    public PacketCaptureDetails(boolean granted, String token, String fileName) {
        this.granted = granted;
        this.token = token;
        this.fileName = fileName;
    }
}


