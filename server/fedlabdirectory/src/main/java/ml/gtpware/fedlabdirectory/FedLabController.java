package ml.gtpware.fedlabdirectory;

import org.springframework.web.bind.annotation.*;

@RestController
public class FedLabController {
    private DirectoryContainer directoryContainer;

    public FedLabController() {
        this.directoryContainer = DirectoryContainer.getInstance();
    }

    @GetMapping("/capabilities")
    String getCapabilities(){
        return directoryContainer.prettyFormattedCapabilities();
    }

    @GetMapping("/devices")
    String getDevices(){
        return directoryContainer.prettyFormattedDevices();
    }

    @RequestMapping(value="/capabilities", method = RequestMethod.POST, produces = "application/json", consumes = "application/json")
    public @ResponseBody void receiveCapability(@RequestBody Capability capability){
        directoryContainer.addCapability(capability);
    }

    @RequestMapping(value="/devices", method = RequestMethod.POST, produces = "application/json", consumes = "application/json")
    public @ResponseBody void receiveDevice(@RequestBody Capability device){
        directoryContainer.addDevice(device);
    }
}
