package ml.gtpware;

import java.io.IOException;
import java.nio.file.*;

import static java.nio.file.StandardWatchEventKinds.ENTRY_MODIFY;

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
            dir.register(watcher, ENTRY_MODIFY);

            System.out.println("Watch Service registered for dir: " + dir.getFileName());

            while (true) {
                WatchKey key;
                try {
                    key = watcher.take();
                } catch (InterruptedException ex) {
                    return;
                }

                for (WatchEvent<?> event : key.pollEvents()) {
                    WatchEvent.Kind<?> kind = event.kind();

                    @SuppressWarnings("unchecked")
                    WatchEvent<Path> ev = (WatchEvent<Path>) event;
                    Path fileName = ev.context();

                    System.out.println(kind.name() + ": " + fileName);

                    if (kind == ENTRY_MODIFY && fileName.toString().equals("device_directory")) {
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
