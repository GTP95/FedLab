#!/bin/bash

# Script has to be run as sudo to modify arptables
if [ "$EUID" -ne 0 ]
  then echo "Please run the script as root (sudo init.sh ...)"
  exit
fi

# Fill in the router's mac address
ROUTER="6B:9C:8A:24:A5:7B"

# Could also include a port number if neccessary
# Fill in the mac address of the machine that runs Vagrant
VAGRANT="14:33:f3:0d:eb:03"


# Allow the router to send packets
arptables -A OUTPUT --source-mac $ROUTER -j ACCEPT
arptables -A INPUT --destination-mac $ROUTER -j ACCEPT

# Allow ssh for Vagrant
arptables -A OUTPUT --source-mac $VAGRANT -j ACCEPT
arptables -A INPUT --destination-mac $VAGRANT -j ACCEPT

# Change all policies to drop all packets
arptables -P INPUT DROP
arptables -P OUTPUT DROP
arptables -P FORWARD DROP

