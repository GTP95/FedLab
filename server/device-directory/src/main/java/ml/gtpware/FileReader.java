package ml.gtpware;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import com.github.lalyos.jfiglet.FigletFont;
import com.google.gson.*;


public class FileReader {
    private Path filePath;
    private String fileContent, prettyFormattedDeviceDirectoryContent;
    private static FileReader instance;
    private final Gson gson;

    private FileReader(){
        this.prettyFormattedDeviceDirectoryContent="Waiting for data";
        this.gson=new Gson();
        this.filePath=Path.of("/server-subscriber/device_directory");
        try {
            File file=new File("/server-subscriber/device_directory");
            if(file.exists() && file.length()!=0){
                reloadFile();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static FileReader getInstance(){
        if (instance==null){
            instance=new FileReader();
        }
        return instance;
    }


    synchronized void reloadFile() throws IOException {
        fileContent = Files.readString(filePath);
        String[] jsonStringsArray = fileContent.split("}");
        CapabilityDirectoryContainer capabilityDirectoryContainer=new CapabilityDirectoryContainer();    //Removes all elements before adding the content of the device directory, this way I'm syncing also removal of capabilities
        for (int index = 0; index < jsonStringsArray.length - 1; index++) {  //I have to skip the last element as it doesn't contain a json, artifact of string splitting
            jsonStringsArray[index] += "}";   //Splitting a string like above removes terminating '}', have to add this again
            Capability capability=gson.fromJson(jsonStringsArray[index], Capability.class);
            if(capability.is_capability) capabilityDirectoryContainer.addCapability(capability);
            else capabilityDirectoryContainer.addDevice(capability);
        }




        prettyFormattedDeviceDirectoryContent= FigletFont.convertOneLine("FedLab directory")+"\n\n\n"+capabilityDirectoryContainer.prettyFormattedCapabilities()+capabilityDirectoryContainer.prettyFormattedDevices();
    }

    synchronized String readFile(){
        return prettyFormattedDeviceDirectoryContent;
    }
}
