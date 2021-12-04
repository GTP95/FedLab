package ml.gtpware.fedlabdirectory;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Objects;

public class Capability{
    //Not following Java convention to reflect the name of the Json's fields
    @JsonProperty("party_name") String party_name;
    @JsonProperty("gateway_ip") String ip;
    @JsonProperty("gateway_port") int gateway_port;
    @JsonProperty("capability_name") String capability_name;
    @JsonProperty("description") String description;
    @JsonProperty("is_capability") boolean is_capability;
    @JsonProperty("uuid") String uuid;
    @JsonProperty("isOnline") boolean isOnline;

    public Capability(String party_name, String ip, int port, String capability_name, String description, boolean is_capability) {
        this.party_name = party_name;
        this.ip = ip;
        this.gateway_port = port;
        this.capability_name = capability_name;
        this.description = description;
        this.is_capability=is_capability;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Capability that = (Capability) o;
        return gateway_port == that.gateway_port &&
                is_capability == that.is_capability &&
                party_name.equals(that.party_name) &&
                ip.equals(that.ip) &&
                capability_name.equals(that.capability_name) &&
                Objects.equals(description, that.description) &&
                Objects.equals(uuid, that.uuid);
    }

    @Override
    public int hashCode() {
        return Objects.hash(party_name, ip, gateway_port, capability_name, description, is_capability, uuid);
    }
}
