package ml.gtpware;

public class Capability {
    //Not following Java convention to reflect the name of the Json's fields
    String party_name;
    String device;
    String capability_name;
    String capability_id;
    String capability_desc;

    public Capability(String party_name, String device, String capability_name, String capability_id, String capability_desc) {
        this.party_name = party_name;
        this.device = device;
        this.capability_name = capability_name;
        this.capability_id = capability_id;
        this.capability_desc = capability_desc;
    }
}


