package ml.gtpware;

import java.util.Objects;

public class Capability implements Comparable<Capability>{
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

    @Override
    public int compareTo(Capability capability) {   //Used to nicely sort the capabilities in the capabilities directory
        if(this.equals(capability)) return 0;
        if(this.party_name.compareTo(capability.party_name)<0) return -1;
        else if(this.party_name.compareTo(capability.party_name)>0) return 1;
        else{   //Same party_name
            if(this.capability_name.compareTo(capability.capability_name)<0) return -1;
            else if(this.capability_name.compareTo(capability.capability_name)>0) return 1;
            else {  //Same party_name and capability_name
                if(this.port>capability.port) return 1;
                else return 0;
            }
        }
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Capability that = (Capability) o;
        return port == that.port && party_name.equals(that.party_name) && gateway_ip.equals(that.gateway_ip) && capability_name.equals(that.capability_name) && description.equals(that.description);
    }

    @Override
    public int hashCode() {
        return Objects.hash(party_name, gateway_ip, port, capability_name, description);
    }
}


