#!/bin/bash

# To run: sudo manage_acl.sh add/remove mac_address

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

IP_RANGE=$(grep range /etc/dhcp/dhcpd.conf | cut -c 9- | rev | cut -c 2- | rev)

CURRENT_TIME=$(date +%s)

MAC="$2"
# If the mac uses - instead of : replace them
NEW_MAC="${MAC//-/:}"

if [[ $NEW_MAC =~ ^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$ ]]
    then echo "MAC address is valid"
else
    echo "MAC address is invalid"
    exit
fi

# Determine if the first argument has been set correctly
if [ "$1" = 'add' ]
    then echo "MAC address was added to the ACL"
    IP_ADDR=`./get_random_ip.py $IP_RANGE`
    # Add mac addresses to the file
    echo "$IP_ADDR $NEW_MAC $CURRENT_TIME offline" >> $file_name

	  # Allow the device to get an IP address via DHCP
    cp /etc/dhcp/dhcpd_base.conf /etc/dhcp/dhcpd.conf
    ./configure_dhcp.py
    sudo systemctl restart isc-dhcp-server

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
    ./configure_dhcp.py
    sudo systemctl restart isc-dhcp-server

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
