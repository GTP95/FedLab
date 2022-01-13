#!/bin/bash

INTERNET_ADAPTER=enp0s3
VM_SUBNET_ADAPTER=enp0s8
VPN_ADAPTER=tun0

# Script has to be run as sudo to modify iptables
if [ "$EUID" -ne 0 ]
  then echo "Please run the script as root (sudo iptables.sh ...)"
  exit
fi

iptables --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables --table nat -F
iptables --table nat -X

iptables -P INPUT DROP
iptables -P OUTPUT ACCEPT  # for now, accept requests originating from the VM. TODO: refine
iptables -P FORWARD DROP


# ----INPUT----
# allow established sessions to receive traffic
iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT

# allow incoming connections from localhost
iptables -A INPUT -i lo -j ACCEPT

# allow incoming ICMP echo requests from the VPN and VM subnet
iptables -A INPUT -i $VPN_ADAPTER -p icmp --icmp-type 8 -j ACCEPT
iptables -A INPUT -i $VM_SUBNET_ADAPTER -p icmp --icmp-type 8 -j ACCEPT

# allow SSH from the host PC. Needed by Vagrant to provision VM
iptables -A INPUT -i $INTERNET_ADAPTER -p tcp --dport 22 -j ACCEPT
# ----/INPUT----


# ----FORWARD----
# allow established incoming connections to IoT devices
iptables -A FORWARD -o $VM_SUBNET_ADAPTER -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT

# drop traffic from IoT devices to the IP range of your organisation
iptables -A FORWARD -i $VM_SUBNET_ADAPTER -o $INTERNET_ADAPTER -d $1 -j DROP

# allow traffic from IoT devices otherwise
iptables -A FORWARD -i $VM_SUBNET_ADAPTER -j ACCEPT
# ----/FORWARD----


# enable NAT for destinations outside of the lab
iptables -t nat -A POSTROUTING -o $INTERNET_ADAPTER -j MASQUERADE


echo "saving"
iptables-save > /etc/iptables.rules
echo "done"
