package ml.gtpware.fedlabdirectory;

import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.Iterator;

public class DirectoryContainer {
    private final ArrayList<ArrayList<Capability>> capabilities, devices;
    private static DirectoryContainer instance;

    private DirectoryContainer(){
        capabilities=new ArrayList<ArrayList<Capability>>();
        devices=new ArrayList<ArrayList<Capability>>();
    }

    public static DirectoryContainer getInstance(){
        if(instance==null) instance=new DirectoryContainer();
        return instance;
    }

    public synchronized void addCapability(Capability capability){
        if(capabilities.isEmpty()){
            capabilities.add(new ArrayList<Capability>());
            capabilities.get(0).add(capability);
            return;
        }
        //look if the party sharing the capability is already present. If so, add the capability to the party's ArrayList
        for(ArrayList<Capability> arrayList : capabilities){
            if(!arrayList.isEmpty() && arrayList.get(0).party_name.equals(capability.party_name)){
                arrayList.add(capability);
                return;
            }
        }

        //Else the party isn't already present, so we need ot create a new ArrayList for that party and add the capability there
        capabilities.add(new ArrayList<Capability>());
        capabilities.get(capabilities.size()-1).add(capability);
    }

    public synchronized void addDevice(@NotNull Capability device){
        if(devices.isEmpty()){
            devices.add(new ArrayList<Capability>());
            devices.get(0).add(device);
            return;
        }

        //Look if the party sharing the device is already present. If yes, add the capability to its ArrayList
        for(ArrayList<Capability> arrayList : devices){
            if(!arrayList.isEmpty() && arrayList.get(0).party_name.equals(device.party_name)){
                arrayList.add(device);
                return;
            }
        }

        //Else the party isn't already there, so we need to create a new ArrayList and add there the device
        devices.add(new ArrayList<Capability>());
        devices.get(devices.size()-1).add(device);
    }

    public synchronized String prettyFormattedCapabilities(){
        String string=new String("CAPABILITIES:\n");
        for(ArrayList<Capability> arrayList : capabilities){
            if(!arrayList.isEmpty()) {


                string += "Party: " + arrayList.get(0).party_name + "\n";
                for (Capability capability : arrayList) {
                    string += ("\t" + "Capability name: " + capability.capability_name + "\n" +
                            "\t" + "Capability description: " + capability.description + "\n" +
                            "\t" + "Capability IP: " + capability.ip + "\n" +
                            "\t" + "Capability port: " + capability.gateway_port + "\n" +
                            "\t" + "Is online: " + capability.isOnline + "\n\n");
                }
            }
        }
        return string;

    }

    public synchronized String prettyFormattedHTMLcapabilities(){
        String string=new String("CAPABILITIES:<br>");
        for(ArrayList<Capability> arrayList : capabilities){
            if(!arrayList.isEmpty()) {
                string += "Party: " +  arrayList.get(0).party_name + "<br>";
                for (Capability capability : arrayList) {
                    string += ("&emsp;" + "Capability name: " + capability.capability_name + "<br>" +
                            "&emsp;" + "Capability description: " + capability.description + "<br>" +
                            "&emsp;" + "Capability IP: " + capability.ip + "<br>" +
                            "&emsp;" + "Capability port: " + capability.gateway_port + "<br>" +
                            "&emsp;" + "Is online: " + capability.isOnline + "<br><br>");
                }
            }
        }
        return string;

    }

    public synchronized String prettyFormattedHTMLonlineCapabilities(){
        String string=new String("CAPABILITIES:<br>");
        for(ArrayList<Capability> arrayList : capabilities){
            if(!arrayList.isEmpty()) {
                string += "Party: " + arrayList.get(0).party_name + "<br>";
                for (Capability capability : arrayList) {
                    if (capability.isOnline)
                        string += ("&emsp;" + "Capability name: " + capability.capability_name + "<br>" +
                                "&emsp;" + "Capability description: " + capability.description + "<br>" +
                                "&emsp;" + "Capability IP: " + capability.ip + "<br>" +
                                "&emsp;" + "Capability port: " + capability.gateway_port + "<br>" +
                                "&emsp;" + "Is online: " + capability.isOnline + "<br><br>");
                }
            }
        }
        return string;
    }

    public synchronized String prettyFormattedDevices(){
        String string=new String("DEVICES:\n");
        for(ArrayList<Capability> arrayList : devices){
            if(!arrayList.isEmpty()) {
                string += "Party: " + arrayList.get(0).party_name + "\n";

                for (Capability capability : arrayList) {
                    if (capability.description == null)
                        string += ("\t" + "Device name: " + capability.capability_name + "\n" +
                                "\t" + "Device IP: " + capability.ip + "\n\n");
                    else
                        string += ("\t" + "Device name: " + capability.capability_name + "\n" +
                                "\t" + "Device IP: " + capability.ip + "\n" +
                                "\t"+"Description: " + capability.description + "\n" +
                               "\t"+ "Is online: " + capability.isOnline + "\n\n");
                }
            }
        }
        return string;
    }

    public synchronized String prettyFormattedHTMLdevices(){
        String string=new String("DEVICES:<br>");
        for(ArrayList<Capability> arrayList : devices){
            if(!arrayList.isEmpty()) {
                string += "Party: " + arrayList.get(0).party_name + "<br>";
                for (Capability capability : arrayList) {
                    if (capability.description == null)
                        string += ("&emsp;" + "Device name: " + capability.capability_name + "<br>" +
                                "&emsp;" + "Device IP: " + capability.ip + "<br><br>");
                    else
                        string += ("&emsp;" + "Device name: " + capability.capability_name + "<br>" +
                                "&emsp;" + "Device IP: " + capability.ip + "<br>" +
                                "&emsp;" + "Description: " + capability.description + "<br>" +
                                "&emsp;" + "Is online: " + capability.isOnline + "<br><br>");
                }
            }
        }
        return string;
    }

    public synchronized String prettyFormattedHTMLonlineDevices(){
        String string=new String("DEVICES:<br>");
        for(ArrayList<Capability> arrayList : devices){
            if(!arrayList.isEmpty()) {
                string += "Party: " + arrayList.get(0).party_name + "<br>";
                for (Capability capability : arrayList) {
                    if (capability.description == null && capability.isOnline)
                        string += ("&emsp;" + "Device name: " + capability.capability_name + "<br>" +
                                "&emsp;" + "Device IP: " + capability.ip + "<br><br>");
                    else if (capability.isOnline)
                        string += "&emsp;" + "Device name: " + capability.capability_name + "<br>" +
                                "&emsp;" + "Device IP: " + capability.ip + "<br>" +
                                "&emsp;" + "Description: " + capability.description + "<br>" +
                                "&emsp;" + "Is online: " + true + "<br><br>";
                }
            }
        }
        return string;
    }

    public ArrayList<ArrayList<Capability>> getCapabilities() { //retuns an immutable reference, no need for synchronization
        return capabilities;
    }

    public ArrayList<ArrayList<Capability>> getDevices() {  //retuns an immutable reference, no need for synchronization
        return devices;
    }

    public synchronized void statusUpdate(@NotNull StatusUpdate statusUpdate){    //updates the online status of a capability or device
        for(ArrayList<Capability> arrayList : capabilities){
                for (Capability capability : arrayList){ //There can be multiple capabilities per IP, so we need to check all of them
                    if(capability.ip.equals(statusUpdate.ip)){
                        capability.isOnline=statusUpdate.isOnline;
                    }
                }
        }

        for(ArrayList<Capability> arrayList : devices){
            for (Capability device : arrayList){
                if(device.ip.equals(statusUpdate.ip)){
                    device.isOnline=statusUpdate.isOnline;
                    return; //there is only one device per IP, so we can return here.
                }
            }
        }
    }

    public synchronized void removeDevice(@NotNull RemoveRequest request){
        outer: for(Object arraylist : devices){    //First, find and remove the device
            for(Capability device : (ArrayList<Capability>)arraylist){
                if(device.ip.equals(request.identifier)){
                    ((ArrayList<Capability>) arraylist).remove(device);
                    break outer;
                }
            }
        }

        for (ArrayList<Capability> arraylist : capabilities){  // then remove all associated capabilities
            for(Iterator<Capability> iterator=arraylist.iterator(); iterator.hasNext();){   //Have to use an iterator here to avoid ConcurrentModificationException
                Capability capability=iterator.next();
                if(capability.ip.equals(request.identifier)){
                    iterator.remove();
                }
            }
        }
    }

    public synchronized void removeCapability(@NotNull RemoveRequest request){
        for(ArrayList<Capability> arraylist : capabilities){
            for(Capability capability : arraylist){
                if(capability.uuid.equals(request.identifier)){
                    arraylist.remove(capability); //Again assuming no duplicates TODO: prevent duplicates
                    return;
                }
            }
        }
    }

}
