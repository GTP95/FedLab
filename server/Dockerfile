FROM python:3.9.5-buster

# Install server_subscriber.py's dependencies
RUN pip install paho-mqtt argparse
RUN mkdir /server-subscriber

# Install & configure Java 11
ENV JAVA_HOME="/usr/lib/jvm/default-jvm/"
RUN apk add openjdk11
ENV PATH=$PATH:${JAVA_HOME}/bin

# Copy the needed software
COPY server_subscriber.py /server-subscriber/server_subscriber.py
COPY Device\ Directory/out/artifacts/Device_Directory_jar/Device\ Directory.jar /server-subscriber/device_directory.jar

# Execute software
CMD python /server-subscriber/server_subscriber.py -s mqtt -p 1883
CMD java -jar /server-subscriber/device_directory.jar
