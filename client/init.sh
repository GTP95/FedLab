#!/bin/bash

# Script has to be run as sudo to modify arptables
if [ "$EUID" -ne 0 ]
  then echo "Please run the script as root (sudo init.sh ...)"
  exit
fi

# Fill in the router's mac address
ROUTER="6B:9C:8A:24:A5:7B"

# Vagrant static mac addresses
VAGRANT_LOCAL="52:54:00:12:35:02"
VAGRANT_OUTSIDE="52:54:00:12:35:03"


# Allow the router to send packets
arptables -A OUTPUT --source-mac $ROUTER -j ACCEPT
arptables -A INPUT --destination-mac $ROUTER -j ACCEPT

# Allow ssh for Vagrant
arptables -A OUTPUT --source-mac $VAGRANT_LOCAL -j ACCEPT
arptables -A INPUT --destination-mac $VAGRANT_LOCAL -j ACCEPT
arptables -A OUTPUT --source-mac $VAGRANT_OUTSIDE -j ACCEPT
arptables -A INPUT --destination-mac $VAGRANT_OUTSIDE -j ACCEPT

# Change all policies to drop all packets
arptables -P INPUT DROP
arptables -P OUTPUT DROP
#arptables -P FORWARD DROP

