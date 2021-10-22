#!/bin/bash

# Script has to be run as sudo to modify arptables
if [ "$EUID" -ne 0 ]
  then echo "Please run the script as root (sudo init.sh ...)"
  exit
fi

# allow VPN communication
arptables -A OUTPUT -o tun0 -j ACCEPT
arptables -A INPUT -i tun0 -j ACCEPT

# allow communication with the host computer
arptables -A OUTPUT -o enp0s3 -j ACCEPT
arptables -A INPUT -i enp0s3 -j ACCEPT

# allow outgoing communication from the gateway to connected devices
arptables -A OUTPUT -o enp0s8 -j ACCEPT


# Set the policies to drop all packets
arptables -P INPUT DROP
arptables -P OUTPUT DROP
#arptables -P FORWARD DROP
