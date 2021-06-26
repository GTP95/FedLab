package ml.gtpware;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class FileReader {
    private Path filePath;
    private String fileContent;
    private static FileReader instance;

    private FileReader(){
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
    }

    synchronized String readFile(){
        return fileContent;
    }
}
