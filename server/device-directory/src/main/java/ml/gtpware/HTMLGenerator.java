package ml.gtpware;
import org.apache.commons.text.StringEscapeUtils;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class HTMLGenerator {
    public static void generateHTMLDirectory(String title, String capabilities, String devices, String filePath) throws IOException {
        String escapedTitle=StringEscapeUtils.escapeHtml4(title);   //Escape content
        String escapedCapabilities=StringEscapeUtils.escapeHtml4(capabilities);
        String escapedDevices=StringEscapeUtils.escapeHtml4(devices);
        String html="<!DOCTYPE><html><head><title>"+escapedTitle+"</title></head><body>"+escapedCapabilities+
                escapedDevices+ "</body></html>";

        BufferedWriter writer = new BufferedWriter(new FileWriter(filePath, false));    //Write to file, overwrite instead of appending
        writer.write(html);
        writer.close();
    }
}
