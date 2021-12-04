package ml.gtpware.fedlabdirectory;

import com.github.lalyos.jfiglet.FigletFont;
import org.springframework.web.bind.annotation.*;
import org.unbescape.html.HtmlEscape;

import java.io.IOException;
import java.util.ArrayList;

import static org.springframework.web.util.HtmlUtils.htmlEscape;

@RestController
public class FedLabController {
    private final DirectoryContainer directoryContainer;

    public FedLabController() {
        this.directoryContainer = DirectoryContainer.getInstance();
    }

    @GetMapping("/capabilities")
    ArrayList<ArrayList<Capability>> getCapabilities(){
        return directoryContainer.getCapabilities();
    }

    @GetMapping("/devices")
    ArrayList<ArrayList<Capability>> getDevices(){
        return directoryContainer.getDevices();
    }

    @RequestMapping(value = "/HTMLdirectory" , method = RequestMethod.GET, produces = "text/html")
    public String prettyFormattedDirectory(@RequestParam(value = "showOnlineOnly", required = false) String checkboxvalue) {
        String result;
        if(checkboxvalue==null) {

                result = "<html><title>FedLab directory</title>" + directoryContainer.prettyFormattedCapabilities() + directoryContainer.prettyFormattedDevices()+"</html>";

        }
        else {

                result = "<html><title>FedLab directory</title>" + directoryContainer.prettyFormattedOnlineCapabiilities() + directoryContainer.prettyFormattedOnlineDevices()+"</html>";

        }
        return result;
    }

    @RequestMapping(value="/capabilities", method = RequestMethod.POST, produces = "application/json", consumes = "application/json")
    public @ResponseBody void receiveCapability(@RequestBody Capability capability){
        directoryContainer.addCapability(capability);
    }

    @RequestMapping(value="/devices", method = RequestMethod.POST, produces = "application/json", consumes = "application/json")
    public @ResponseBody void receiveDevice(@RequestBody Capability device){
        directoryContainer.addDevice(device);
    }

    @RequestMapping(value="/statusUpdate", method = RequestMethod.POST, produces = "application/json", consumes = "application/json")
    public @ResponseBody void statusUpdate(@RequestBody StatusUpdate statusUpdate){
        directoryContainer.statusUpdate(statusUpdate);
    }

    @RequestMapping(value="/removeDeviceRequest", method = RequestMethod.POST, produces = "application/json", consumes = "application/json")
    public @ResponseBody void removeDevice(@RequestBody RemoveRequest request){
        directoryContainer.removeDevice(request);
    }

    @RequestMapping(value="/removeCapabilityRequest", method = RequestMethod.POST, produces = "application/json", consumes = "application/json")
    public @ResponseBody void removeCapability(@RequestBody RemoveRequest request){
        directoryContainer.removeCapability(request);
    }


}
