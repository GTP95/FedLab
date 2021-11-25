package ml.gtpware;

import org.apache.commons.lang3.RandomStringUtils;

import java.io.IOException;
import java.text.SimpleDateFormat;

//Singleton containing the status, i.e. is a packet capture already in progress? what's the token to stop it?
public class Status {
   private boolean isPacketCaptureInProgress;
   private static Status instance;
   private String token;
   private final String cmdToSniff;
   private Process tcpdump;

   private Status(){
       this.isPacketCaptureInProgress=false;
       this.cmdToSniff="sudo tcpdump -i "+Main.getIface()+" -w ";   //append fileName here
   }

   public static Status getInstance(){
       if(instance.equals(null)) instance=new Status();
       return instance;
   }

    public synchronized PacketCaptureDetails requestPacketCapture() throws IOException {
        if (isPacketCaptureInProgress) return new PacketCaptureDetails(false, null, null);
        String token= RandomStringUtils.random(5, true, true);
        this.token=token;
        String timeStamp = new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss").format(new java.util.Date());
        String fileName=timeStamp+".pcap";
        String command=cmdToSniff+fileName;

        this.tcpdump=Runtime.getRuntime().exec(command); //starts the packet capture

        return new PacketCaptureDetails(true, token, fileName);
    }

    public synchronized boolean stopPacketCapture(String token){
        if(!isPacketCaptureInProgress) return false;
        if(token.equals(this.token)){
            this.tcpdump.destroy(); //WARNING: Whether the process is normally terminated or not is implementation dependent!!! Luckily we're running this inside a VM, so the behavior will be the same for all parties, but be careful in reusing this code elsewhere!!!!
            return true;
        }
        return false;
    }

}
