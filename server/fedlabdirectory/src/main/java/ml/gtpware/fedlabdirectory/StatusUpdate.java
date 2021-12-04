package ml.gtpware.fedlabdirectory;

import com.fasterxml.jackson.annotation.JsonProperty;

public class StatusUpdate {
    @JsonProperty("ip")String ip;
    @JsonProperty("isOnline") boolean isOnline;
}
