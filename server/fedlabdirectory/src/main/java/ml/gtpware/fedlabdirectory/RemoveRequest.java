package ml.gtpware.fedlabdirectory;

import com.fasterxml.jackson.annotation.JsonProperty;

public class RemoveRequest {
    @JsonProperty("identifier") String identifier;
}
