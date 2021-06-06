#!/bin/bash

# To run: sudo arpRules.sh -add/remove mac_address

#TODO: Check if the arptables rules are persistent between sessions/reboots

# Steps for deployment
# apt install arptables

# Standard deny everything policies
# arptables -P INPUT DROP
# arptables -P FORWARD DROP
# arptables -P OUTPUT DROP (Can also be set to accept and just cancel specific requests)
# TODO: Not sure if we can still ssh into it if we set these rules

# Argument 1: -add/-remove to add/remove a rule
# Argument 2: the mac address, can be both with - or :

# Script has to be run as sudo to modify arptables
if [ "$EUID" -ne 0 ]
  then echo "Please run the script as root (sudo ipRules ...)"
  exit
fi

# Generate a text file in which the mac addresses will be stored
# This file will be used for MQTT
# Might even be used to set rules on reboot if there is no other way
file_name="MAC_addresses.txt"
touch $file_name

IP_BROOKER="172.20.0.1"
CURRENT_TIME=$(date +%s)

MAC="$2"
# If the mac uses - instead of : replace them
NEW_MAC="${MAC//-/:}"

# Standard  invalid param
PARAM="-INVALID"
SET=0

# Determine if the first argument has been set correctly
# TODO: Does MQTT also need the timestamp (probably not)
if [ "$1" = '-add' ]
    then echo "Added"
    PARAM="-A"
	# Add mac addresses to the file
	echo "$NEW_MAC $CURRENT_TIME" >> $file_name
    SET=1
	mqtt pub --topic "aclUpdate" --message "A $NEW_MAC" -h "$IP_BROOKER"
elif [ "$1" = '-remove' ]
    then echo "Removed"
    PARAM="-D"
	# Remove mac address and time from the file
	sed -i "/$NEW_MAC/d" $file_name
    SET=1
	mqtt pub --topic "aclUpdate" --message "D $NEW_MAC" -h "$IP_BROOKER"
else
	echo "Please use -remove or -add after ipRules"
    exit
fi

# TODO: Rules can now be double created if the user is not paying attention, this might not be an issue
# Create a rule such that OUT going packets are from a registered IoT device
arptables $PARAM OUTPUT --source-mac $NEW_MAC -j ACCEPT
# Create a rule such that IN going packets are going to a registered IoT device
arptables $PARAM INPUT --destination-mac $NEW_MAC -j ACCEPT





