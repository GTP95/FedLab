#!/bin/bash

# To run: sudo manage_acl.sh add/remove mac_address

#TODO: Check if the arptables rules are persistent between sessions/reboots

# Steps for deployment
# apt install arptables

# Standard deny everything policies
# arptables -P INPUT DROP
# arptables -P FORWARD DROP
# arptables -P OUTPUT DROP (Can also be set to accept and just cancel specific requests)
# TODO: Not sure if we can still ssh into it if we set these rules

# Argument 1: 'add'/'remove' to add/remove a rule
# Argument 2: the mac address, can be both with - or :

# Script has to be run as sudo to modify arptables
if [ "$EUID" -ne 0 ]
  then echo "Please run the script as root (sudo manage_acl.sh ...)"
  exit
fi

# Generate a text file in which the mac addresses will be stored
# This file will be used for MQTT
# Might even be used to set rules on reboot if there is no other way
file_name="MAC_addresses"
touch $file_name

IP_BROOKER="192.168.201.2"
CURRENT_TIME=$(date +%s)

MAC="$2"
# If the mac uses - instead of : replace them
NEW_MAC="${MAC//-/:}"

if [[ $NEW_MAC =~ ^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$ ]]
	then echo "Correct"
else
	echo "MAC address is invalid"
	exit
fi

# Determine if the first argument has been set correctly
# TODO: Does MQTT also need the timestamp (probably not)
if [ "$1" = 'add' ]
    then echo "Added"
	# Add mac addresses to the file
	echo "$NEW_MAC $CURRENT_TIME offline" >> $file_name
	
	# Allow the device to get an IP address via DHCP
    cp /etc/dhcp/dhcpd_base.conf /etc/dhcp/dhcpd.conf
    WORDS=$(cat MAC_addresses)
    for WORD in $WORDS
    do
        if [[ $WORD =~ ^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$ ]]
            then echo -e "\nhost device-`uuidgen` {\n  hardware ethernet $WORD;\n}" >> /etc/dhcp/dhcpd.conf;
        fi
    done
    sudo systemctl restart isc-dhcp-server
	
	mqtt pub --topic "aclUpdate" --message "A $NEW_MAC" -h "$IP_BROOKER"
	
	# TODO: Rules can now be double created if the user is not paying attention, this might not be an issue
	# Create a rule such that OUT going packets are from a registered IoT device
	arptables -A OUTPUT --destination-mac $NEW_MAC -j ACCEPT
	# Create a rule such that IN going packets are going to a registered IoT device
	arptables -A INPUT --source-mac $NEW_MAC -j ACCEPT
elif [ "$1" = 'remove' ]
    then echo "Removed"
	# Remove mac address and time from the file
	sed -i "/$NEW_MAC/d" $file_name
	
	# Remove the device from the DHCP allow-list
    cp /etc/dhcp/dhcpd_base.conf /etc/dhcp/dhcpd.conf
    WORDS=$(cat MAC_addresses)
    for WORD in $WORDS
    do
        if [[ $WORD =~ ^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$ ]]
            then echo -e "\nhost device-`uuidgen` {\n  hardware ethernet $WORD;\n}" >> /etc/dhcp/dhcpd.conf;
        fi
    done
    sudo systemctl restart isc-dhcp-server
	
	mqtt pub --topic "aclUpdate" --message "D $NEW_MAC" -h "$IP_BROOKER"
	# Find line numbers of the specific rules and delete them
	# Get all the arptables with their line numbers
	# Only show that paragraph
	# Grab the lines with the correct src/dst-mac address
	# Only grab the first line
	# Only grab the first character (the line number)
	# Delete that line number
	TEST=$(sudo arptables --list --line-numbers | sed -n '/INPUT/,/^$/p' | grep -i "src-mac $NEW_MAC" | head -n 1 | cut -c-1)
	arptables -D INPUT $TEST
	TEST=$(sudo arptables --list --line-numbers | sed -n '/OUTPUT/,/^$/p' | grep -i "dst-mac $NEW_MAC" | head -n 1 | cut -c-1)
	arptables -D OUTPUT $TEST
else
	echo "Please use 'remove' or 'add' after ipRules"
    exit
fi







