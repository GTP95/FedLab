package ml.gtpware;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;

import com.google.gson.*;

public class FileReader {
    private Path filePath;
    private String fileContent, prettyFormattedDeviceDirectoryContent;
    private HashSet<Capability> capabilitiesSet;    //Using a set to automatically avoid duplicates
    private static FileReader instance;
    private final Gson gson;

    private FileReader(){
        this.prettyFormattedDeviceDirectoryContent="Waiting for data";
        this.capabilitiesSet=new HashSet<>();
        this.gson=new Gson();
        this.filePath=Path.of("/server-subscriber/device_directory");
        try {
            this.fileContent=Files.readString(filePath);
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
        fileContent= Files.readString(filePath);

        String[] jsonStringsArray=fileContent.split("\n");
        capabilitiesSet.clear();    //Removes all elements before adding the content of the device directory, this way I'm syncing also removal of capabilities
        for(String json : jsonStringsArray){
            capabilitiesSet.add(gson.fromJson(json, Capability.class));
        }

        //Present the data in a "pretty" way
        prettyFormattedDeviceDirectoryContent=new String();
        for(Capability capability : capabilitiesSet){
            prettyFormattedDeviceDirectoryContent.concat("Party: " + capability.party_name + "\n" +
                                                         "Device: " + capability.device + "\n" +
                                                         "Capability name: " + capability.capability_name + "\n" +
                                                         "Capability ID:" + capability.capability_id + "\n" +
                                                         "Capability description: " + capability.capability_desc + "\n\n\n");
        }

    }

    synchronized String readFile(){
        return fileContent;
    }
}
