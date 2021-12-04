package ml.gtpware.fedlabdirectory;

import java.util.ArrayList;

public class DirectoryContainer {
    private final ArrayList<ArrayList<Capability>> capabilities, devices;
    private final ArrayList<String> capabilitiesParties, devicesParties;
    private static DirectoryContainer instance;

    private DirectoryContainer(){
        capabilities=new ArrayList<ArrayList<Capability>>();
        devices=new ArrayList<ArrayList<Capability>>();
        capabilitiesParties=new ArrayList<>();
        devicesParties=new ArrayList<>();
    }

    public static DirectoryContainer getInstance(){
        if(instance==null) instance=new DirectoryContainer();
        return instance;
    }

    public void addCapability(Capability capability){
        if(capabilities.isEmpty()){
            capabilities.add(new ArrayList<Capability>());
            capabilities.get(0).add(capability);
            capabilitiesParties.add(capability.party_name);
            return;
        }
        if(capabilitiesParties.contains(capability.party_name)){
            for(Object arrayList : capabilities){
                if(!((ArrayList<Capability>)arrayList).isEmpty() && ((ArrayList<Capability>)arrayList).get(0).party_name.equals(capability.party_name)){
                    ((ArrayList<Capability>)arrayList).add(capability);
                    break;
                }
            }
        }
        else{
            capabilities.add(new ArrayList<Capability>());
            capabilities.get(capabilities.size()-1).add(capability);
            capabilitiesParties.add(capability.party_name);
        }
    }

    public void addDevice(Capability device){
        if(devices.isEmpty()){
            devices.add(new ArrayList<Capability>());
            devices.get(0).add(device);
            devicesParties.add(device.party_name);
            return;
        }
        if(devicesParties.contains(device.party_name)){
            for(Object arrayList : devices){
                if(!((ArrayList<Capability>)arrayList).isEmpty() && ((ArrayList<Capability>)arrayList).get(0).party_name.equals(device.party_name)){
                    ((ArrayList<Capability>)arrayList).add(device);
                    break;
                }
            }
        }
        else {
            capabilities.add(new ArrayList<Capability>());
            devicesParties.add(device.party_name);
        }
    }

    public String prettyFormattedCapabilities(){
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

    public String prettyFormattedHTMLcapabilities(){
        String string=new String("CAPABILITIES:<br>");
        for(Object arrayList : capabilities){
            string+="Party: " + ((ArrayList<Capability>)arrayList).get(0).party_name +"<br>";
            for(Capability capability : (ArrayList<Capability>)arrayList){
                string+=("&emsp;"+"Capability name: "+capability.capability_name+"<br>" +
                        "&emsp;"+"Capability description: "+capability.description+"<br>"+
                        "&emsp;"+"Capability IP: "+capability.ip +"<br>" +
                        "&emsp;"+"Capability port: "+capability.gateway_port+"<br>"+
                        "&emsp;"+"Is online: " +capability.isOnline+"<br><br>");
            }
        }
        return string;

    }

    public String prettyFormattedHTMLonlineCapabiilities(){
        String string=new String("CAPABILITIES:<br>");
        for(Object arrayList : capabilities){
            string+="Party: " + ((ArrayList<Capability>)arrayList).get(0).party_name +"<br>";
            for(Capability capability : (ArrayList<Capability>)arrayList){
                if(capability.isOnline)
                    string+=("&emsp;"+"Capability name: "+capability.capability_name+"<br>" +
                        "&emsp;"+"Capability description: "+capability.description+"<br>"+
                        "&emsp;"+"Capability IP: "+capability.ip +"<br>" +
                        "&emsp;"+"Capability port: "+capability.gateway_port+"<br>"+
                        "&emsp;"+"Is online: " +capability.isOnline+"<br><br>");
            }
        }
        return string;
    }

    public String prettyFormattedDevices(){
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
                                "Description: " + capability.description + "\n" +
                                "Is online: " + capability.isOnline + "\n\n");
                }
            }
        }
        return string;
    }

    public String prettyFormattedHTMLdevices(){
        String string=new String("DEVICES:<br>");
        for(Object arrayList : devices){
            string+="Party: " + ((ArrayList<Capability>)arrayList).get(0).party_name +"<br>";
            for(Capability capability : (ArrayList<Capability>)arrayList){
                if(capability.description==null)
                    string+=("&emsp;"+"Device name: "+capability.capability_name+"<br>" +
                            "&emsp;"+"Device IP: "+capability.ip +"<br><br>");
                else
                    string+=("&emsp;"+"Device name: "+capability.capability_name+"<br>" +
                            "&emsp;"+"Device IP: "+capability.ip +"<br>"+
                            "Description: "+capability.description+"<br>"+
                            "Is online: "+capability.isOnline+"<br><br>");
            }
        }
        return string;
    }

    public String prettyFormattedHTMLonlineDevices(){
        String string=new String("DEVICES:<br>");
        for(Object arrayList : devices){
            string+="Party: " + ((ArrayList<Capability>)arrayList).get(0).party_name +"<br>";
            for(Capability capability : (ArrayList<Capability>)arrayList){
                if(capability.description==null && capability.isOnline)
                    string+=("&emsp;"+"Device name: "+capability.capability_name+"<br>" +
                            "&emsp;"+"Device IP: "+capability.ip +"<br><br>");
                else if(capability.isOnline)
                    string+= "&emsp;"+"Device name: "+capability.capability_name+"<br>" +
                            "&emsp;"+"Device IP: "+capability.ip +"<br>"+
                            "Description: "+capability.description+"<br>"+
                            "Is online: "+ true +"<br><br>";
            }
        }
        return string;
    }

    public ArrayList<ArrayList<Capability>> getCapabilities() {
        return capabilities;
    }

    public ArrayList<ArrayList<Capability>> getDevices() {
        return devices;
    }

    public void statusUpdate(StatusUpdate statusUpdate){    //updates the online status of a capability or device
        for(Object arrayList : capabilities){
            for (Capability capability : (ArrayList<Capability>)arrayList){
                if(capability.ip.equals(statusUpdate.ip)){
                    capability.isOnline=statusUpdate.isOnline;
                    return;
                }
            }
        }

        for(Object arrayList : devices){
            for (Capability device : (ArrayList<Capability>)arrayList){
                if(device.ip.equals(statusUpdate.ip)){
                    device.isOnline=statusUpdate.isOnline;
                    return;
                }
            }
        }
    }

    public void removeDevice(RemoveRequest request){
        outer: for(Object arraylist : devices){    //First, find and remove the device
            for(Capability device : (ArrayList<Capability>)arraylist){
                if(device.ip.equals(request.identifier)){
                    ((ArrayList<Capability>) arraylist).remove(device);
                    break outer;
                }
            }
        }

        for (Object arraylist : capabilities){  // then remove all associated capabilities
            for(Capability capability : (ArrayList<Capability>)arraylist){
                if(capability.ip.equals(request.identifier)){
                    ((ArrayList<Capability>) arraylist).remove(capability);
                }
            }
        }
    }

    public void removeCapability(RemoveRequest request){
        for(Object arraylist : devices){
            for(Capability capability : (ArrayList<Capability>)arraylist){
                if(capability.uuid.equals(request.identifier)){
                    ((ArrayList<Capability>) arraylist).remove(capability); //Again assuming no duplicates TODO: prevent duplicates
                }
            }
        }
    }

}
