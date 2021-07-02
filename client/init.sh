#!/bin/bash

# Script has to be run as sudo to modify arptables
if [ "$EUID" -ne 0 ]
  then echo "Please run the script as root (sudo init.sh ...)"
  exit
fi

arptables -A OUTPUT -o tun0 -j ACCEPT
arptables -A INPUT -i tun0 -j ACCEPT

# Set the policies to drop all packets
arptables -P INPUT DROP
arptables -P OUTPUT DROP
#arptables -P FORWARD DROP

