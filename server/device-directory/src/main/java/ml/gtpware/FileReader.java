package ml.gtpware;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import com.google.gson.*;


public class FileReader {
    private Path filePath;
    private String fileContent, prettyFormattedDeviceDirectoryContent;
    private SortedSet<Capability> capabilitiesSet;    //Using a set to automatically avoid duplicates
    private static FileReader instance;
    private final Gson gson;

    private FileReader(){
        this.prettyFormattedDeviceDirectoryContent="Waiting for data";
        this.capabilitiesSet=new TreeSet<>();
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
        capabilitiesSet.clear();    //Removes all elements before adding the content of the device directory, this way I'm syncing also removal of capabilities
        System.out.println(jsonStringsArray.length);
        for (int index = 0; index < jsonStringsArray.length - 1; index++) {  //I have to skip the last element as it doesn't contain a json, artifact of string splitting
            jsonStringsArray[index] += "}";   //Splitting a string like above removes terminating '}', have to add this again
            System.out.println(jsonStringsArray[index]);
            capabilitiesSet.add(gson.fromJson(jsonStringsArray[index], Capability.class));
        }

        //Present the data in a "pretty" way
        prettyFormattedDeviceDirectoryContent = new String();
        String prettyFormattedCapabilities = "CAPABILITIES:\n";
        String prettyFormattedDevices = "DEVICES:\n";
        Capability previousCapability = capabilitiesSet.first();
        Capability capability;

        //start by constructing capabilities list
        Iterator iterator = capabilitiesSet.iterator();
        while(iterator.hasNext()){ //look for the first capability
            capability = (Capability) iterator.next();
            if (capability.is_capability){
                previousCapability=capability;
                break;
            }
        }

        //construct first entry of the device list:
        prettyFormattedCapabilities += ("Party: " + previousCapability.party_name + "\n" +
                "\tGateway IP: " + previousCapability.gateway_ip + "\n" +
                "\tGateway port: " + previousCapability.gateway_port + "\n" +
                "\tCapability name: " + previousCapability.capability_name + "\n" +
                "\tCapability description: " + previousCapability.description + "\n\n\n");

        iterator.remove();  //remove this capability from the set as we already added it to the list

        //Construct all others entries
        while(iterator.hasNext()) {
            capability = (Capability) iterator.next();
            if (capability.is_capability){
                if (capability.party_name.equals(previousCapability.party_name)) {
                    prettyFormattedCapabilities += ("\tGateway IP: " + capability.gateway_ip + "\n" +
                            "\tGateway port: " + capability.gateway_port + "\n" +
                            "\tCapability name: " + capability.capability_name + "\n" +
                            "\tCapability description: " + capability.description + "\n\n\n");
                } else {
                    prettyFormattedCapabilities += ("Party: " + capability.party_name + "\n" +
                            "\tGateway IP: " + capability.gateway_ip + "\n" +
                            "\tGateway port: " + capability.gateway_port + "\n" +
                            "\tCapability name: " + capability.capability_name + "\n" +
                            "\tCapability description: " + capability.description + "\n\n\n");
                }
                previousCapability=capability;
                iterator.remove();  //Remove the capability we just added to the list from the set of capabilities
            }
        }


        //We now move onto constructing the device list. As all capabilities were removed from the set as we were adding them to the list, we don't need to check if the remains are actually devices: they are guaranteed to be
        //We need a fresh iterator to start from the beginning of the set again
        iterator = capabilitiesSet.iterator();
        previousCapability=capabilitiesSet.first();
        prettyFormattedDevices += ("Party: " + previousCapability.party_name + "\n");
        while (iterator.hasNext()){
            capability= (Capability) iterator.next();
            if (capability.party_name.equals(previousCapability.party_name))
                prettyFormattedDevices += ("\tDevice IP: " + capability.gateway_ip + "\n" +
                        "\tDevice name: " + capability.capability_name + "\n");
             else
                prettyFormattedDevices += ("Party: " + capability.party_name + "\n" +
                        "\tDevice IP: " + capability.gateway_ip + "\n" +
                        "\tDevice name: " + capability.capability_name + "\n" +
                        "\n\n\n");

            previousCapability=capability;
            //No need to remove capabilities now as the set will be discarded later anyway
        }


        prettyFormattedDeviceDirectoryContent=prettyFormattedCapabilities + prettyFormattedDevices;
    }

    synchronized String readFile(){
        return prettyFormattedDeviceDirectoryContent;
    }
}
