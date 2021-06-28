FROM python:3.9.5-buster

# Install server_subscriber.py's dependencies
RUN pip install paho-mqtt argparse
RUN mkdir /server-subscriber

# Install & configure Java 11
ENV JAVA_HOME="/usr/lib/jvm/default-jvm/"
RUN apt-get -y update && apt-get -y install openjdk-11-jdk
ENV PATH=$PATH:${JAVA_HOME}/bin

# Copy the needed software
COPY server_subscriber.py /server-subscriber/server_subscriber.py
COPY device-directory/out/artifacts/Device_Directory_jar/device_directory.jar /server-subscriber/device_directory.jar
COPY start.sh /server-subscriber/start.sh

run chmod +x /server-subscriber/start.sh

# Execute software
CMD /server-subscriber/start.sh
