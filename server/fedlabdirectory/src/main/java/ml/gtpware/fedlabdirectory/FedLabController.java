package ml.gtpware.fedlabdirectory;

import com.github.lalyos.jfiglet.FigletFont;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.ArrayList;

@RestController
public class FedLabController {
    private DirectoryContainer directoryContainer;

    public FedLabController() {
        this.directoryContainer = DirectoryContainer.getInstance();
    }

    @GetMapping("/capabilities")
    ArrayList getCapabilities(){
        return directoryContainer.getCapabilities();
    }

    @GetMapping("/devices")
    ArrayList getDevices(){
        return directoryContainer.getDevices();
    }

    @GetMapping("/directory")
    String prettyFormattedDirectory(){
        try {
            return FigletFont.convertOneLine("FedLab directory") + directoryContainer.prettyFormattedCapabilities() + directoryContainer.prettyFormattedDevices();
        } catch (IOException e) {
            return "FedLab directory" + directoryContainer.prettyFormattedCapabilities() + directoryContainer.prettyFormattedDevices();
        }
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
