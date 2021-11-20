#!/bin/bash
python /server-subscriber/server_subscriber.py -s mqtt -p 1883 & java -jar /server-subscriber/device_directory.jar & service apache2 start

