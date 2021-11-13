package ml.gtpware;

public class Capability {
    //Not following Java convention to reflect the name of the Json's fields
    String party_name;
    String gateway_ip;
    int port;
    String capability_name;
    String description;

    public Capability(String party_name, String gateway_ip, int port, String capability_name, String description) {
        this.party_name = party_name;
        this.gateway_ip = gateway_ip;
        this.port = port;
        this.capability_name = capability_name;
        this.description = description;
    }
}


