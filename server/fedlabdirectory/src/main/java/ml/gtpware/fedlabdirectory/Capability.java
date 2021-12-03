package ml.gtpware.fedlabdirectory;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Objects;

public class Capability implements Comparable<Capability>{
    //Not following Java convention to reflect the name of the Json's fields
    @JsonProperty("party_name") String party_name;
    @JsonProperty("gateway_ip") String gateway_ip;
    @JsonProperty("gateway_port") int gateway_port;
    @JsonProperty("capability_name") String capability_name;
    @JsonProperty("description") String description;
    @JsonProperty("is_capability") boolean is_capability;

    public Capability(String party_name, String gateway_ip, int port, String capability_name, String description, boolean is_capability) {
        this.party_name = party_name;
        this.gateway_ip = gateway_ip;
        this.gateway_port = port;
        this.capability_name = capability_name;
        this.description = description;
        this.is_capability=is_capability;
    }

    @Override
    public int compareTo(Capability capability) {   //Used to nicely sort the capabilities in the capabilities directory
        if(this.equals(capability)) return 0;
        if(this.party_name.compareTo(capability.party_name)<0) return -1;
        else if(this.party_name.compareTo(capability.party_name)>0) return 1;
        else{   //Same party_name
            if(this.capability_name.compareTo(capability.capability_name)<0) return -1;
            else if(this.capability_name.compareTo(capability.capability_name)>0) return 1;
            else {  //Same party_name and capability_name. This shouldn't happen for devices so it is "safe" to leave it this way
                if(this.gateway_port>capability.gateway_port) return 1;
                else return 0;
            }
        }
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Capability that = (Capability) o;
        return gateway_port == that.gateway_port && is_capability == that.is_capability && party_name.equals(that.party_name) && gateway_ip.equals(that.gateway_ip) && capability_name.equals(that.capability_name) && Objects.equals(description, that.description);
    }

    @Override
    public int hashCode() {
        return Objects.hash(party_name, gateway_ip, gateway_port, capability_name, description, is_capability);
    }
}
