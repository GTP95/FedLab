package ml.gtpware;

import java.util.ArrayList;

public class CapabilityDirectoryContainer {
    private ArrayList capabilities, devices;
    private ArrayList<String> capabilitiesParties, devicesParties;


    public void CapabilityDirectoryContainer(){
        capabilities=new ArrayList<ArrayList<Capability>>();
        devices=new ArrayList<ArrayList<Capability>>();
        capabilitiesParties=new ArrayList<>();
        devicesParties=new ArrayList<>();
    }

    public void addCapability(Capability capability){
        if(capabilities.isEmpty()){
            capabilities.add(new ArrayList<Capability>());
            ((ArrayList<Capability>)capabilities.get(0)).add(capability);
            capabilitiesParties.add(capability.party_name);
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
            ((ArrayList<Capability>)capabilities.get(capabilities.size()-1)).add(capability);
            capabilitiesParties.add(capability.party_name);
        }
    }

    public void addDevice(Capability device){
        if(devices.isEmpty()){
            devices.add(new ArrayList<Capability>());
            ((ArrayList<Capability>)devices.get(0)).add(device);
            devicesParties.add(device.party_name);
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
        for(Object arrayList : capabilities){
                string+="Party: " + ((ArrayList<Capability>)arrayList).get(0).party_name +"\n";
                for(Capability capability1 : (ArrayList<Capability>)arrayList){
                    string+=("\t"+"Capability name: "+capability1.capability_name+"\n" +
                            "\t"+"Capability description: "+capability1.description+"\n"+
                            "\t"+"Gateway IP: "+capability1.gateway_ip+"\n" +
                            "\t"+"Gateway port: "+capability1.gateway_port+"\n\n");
                }
            }
        return string;

    }

}

