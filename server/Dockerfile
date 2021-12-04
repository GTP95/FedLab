FROM ubuntu:20.04

# Install server_subscriber.py's dependencies
RUN mkdir /server-subscriber

# Install & configure Java 11
ENV JAVA_HOME="/usr/lib/jvm/default-jvm/"
RUN apt-get -y update && apt-get -y install openjdk-11-jdk
ENV PATH=$PATH:${JAVA_HOME}/bin

# Copy the needed software
ARG src="fedlabdirectory/target/fedlabdirectory-0.0.1-SNAPSHOT.jar"
COPY ${src} /server-subscriber/fedlab_directory.jar
COPY start.sh /server-subscriber/start.sh

run chmod +x /server-subscriber/start.sh

# Execute software
CMD /server-subscriber/start.sh
