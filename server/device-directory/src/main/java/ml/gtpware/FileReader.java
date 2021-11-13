package ml.gtpware;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Type;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.List;

import com.google.gson.*;
import com.google.gson.reflect.TypeToken;

public class FileReader {
    private Path filePath;
    private String fileContent, prettyFormattedDeviceDirectoryContent;
    private HashSet<Capability> capabilitiesSet;    //Using a set to automatically avoid duplicates
    private static FileReader instance;
    private final Gson gson;
    private static final Type CapabilitiesList = new TypeToken<List<Capability>>() {
    }.getType();

    private FileReader(){
        this.prettyFormattedDeviceDirectoryContent="Waiting for data";
        this.capabilitiesSet=new HashSet<>();
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
        fileContent= Files.readString(filePath);
        String[] jsonStringsArray=fileContent.split("}");
        capabilitiesSet.clear();    //Removes all elements before adding the content of the device directory, this way I'm syncing also removal of capabilities
        System.out.println(jsonStringsArray.length);
        for(int index=0; index<jsonStringsArray.length-1;index++){  //I have to skip the last element as it doesn't contain a json, artifact of string splitting
            jsonStringsArray[index]+="}";   //Splitting a string like above removes terminating '}', have to add this again
            //json.concat("}vdvdsv"); //Splitting the string like above removes the closing bracket
            System.out.println(jsonStringsArray[index]);
            capabilitiesSet.add(gson.fromJson(jsonStringsArray[index], Capability.class));
        }

        //Present the data in a "pretty" way
        prettyFormattedDeviceDirectoryContent=new String();
        for(Capability capability : capabilitiesSet){
            prettyFormattedDeviceDirectoryContent+=("Party: " + capability.party_name + "\n" +
                                                         "\tGateway IP: " + capability.gateway_ip + "\n" +
                                                         "\tGateway port: " + capability.port + "\n" +
                                                         "\tCapability name: " + capability.capability_name + "\n" +
                                                         "\tCapability description: " + capability.description + "\n\n\n");
        }

    }

    synchronized String readFile(){
        return prettyFormattedDeviceDirectoryContent;
    }
}
