package ml.gtpware;

import java.io.IOException;
import java.nio.file.*;

import static java.nio.file.StandardWatchEventKinds.*;

public class ModificationListener implements Runnable{
    FileReader fileReader;

    public ModificationListener(FileReader fileReader) {
        this.fileReader=fileReader;
    }

    @Override
    public void run() {
        try {
            WatchService watcher = FileSystems.getDefault().newWatchService();
            Path dir = Paths.get("/server-subscriber");
            dir.register(watcher, ENTRY_CREATE, ENTRY_DELETE, ENTRY_MODIFY, OVERFLOW);  //At a certain point we started having a problem where sometimes the file didn't get reloaded (we where listening for modifications). This is why to be sure we're registering for all possible events. Not optimal, but robust

            System.out.println("Watch Service registered for dir: " + dir.getFileName());

            while (true) {
                WatchKey key;
                try {
                    key = watcher.take();
                } catch (InterruptedException ex) {
                    return;
                }

                for (WatchEvent<?> event : key.pollEvents()) {  //Here we don't check anymore for the kind of event, but only if it is about our file. Again not optimal but roboust, to avoid missing updates

                    @SuppressWarnings("unchecked")
                    WatchEvent<Path> ev = (WatchEvent<Path>) event;
                    Path fileName = ev.context();


                    if (fileName.toString().equals("device_directory")) {
                        fileReader.reloadFile();
                    }
                }

                boolean valid = key.reset();
                if (!valid) {
                    break;
                }
            }

        } catch (IOException ex) {
            System.err.println(ex);
        }
    }
}
