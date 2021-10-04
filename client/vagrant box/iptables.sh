#!/bin/bash
iptables --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables --table nat -F
iptables --table nat -X

iptables -P INPUT DROP
iptables -P OUTPUT DROP

# allow connections from localhost
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# EDIT THE FOLLOWING TWO LINES. Make sure that the gateway can communicate within your own network
iptables -A INPUT -s <YOUR_IP_RANGE> -j ACCEPT
iptables -A OUTPUT -d <YOUR_IP_RANGE> -j ACCEPT

# for now, accept requests from the gateway. TODO: refine or remove
iptables -A OUTPUT -j ACCEPT

# allow established sessions to receive traffic
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# allow TUN such that the VPN connection works
iptables -A INPUT -i tun+ -j ACCEPT
iptables -A FORWARD -i tun+ -j ACCEPT
iptables -A FORWARD -o tun+ -j ACCEPT
iptables -t nat -A POSTROUTING -o tun+ -j MASQUERADE
iptables -A OUTPUT -o tun+ -j ACCEPT

# allow VPN connection
iptables -I OUTPUT -p udp --destination-port 1194 -m comment --comment "Allow VPN connection" -j ACCEPT
iptables -I OUTPUT -p udp --destination-port 53 -m comment --comment "Allow DNS" -j ACCEPT

# EDIT THE FOLLOWING LINE. Allow SSH from/to local network. Needed by Vagrant to provision VM
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT

# allow communication with devices in the lab LAN
iptables -A OUTPUT -o enp0s8 -j ACCEPT
iptables -A INPUT -i enp0s8 -j ACCEPT

# convert local lab IP of IoT device to IP of the gateway
iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE

# allow established incoming connections to IoT devices
iptables -A FORWARD -i enp0s3 -o enp0s8 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT

# EDIT THE FOLLOWING LINE. drop traffic from IoT devices to your own LAN range
iptables -A FORWARD -i enp0s8 -o enp0s3 -d <YOUR_IP_RANGE> -j DROP

# accept remaining traffic from IoT devices (i.e. everything except your own LAN range)
iptables -A FORWARD -i enp0s8 -o enp0s3 -j ACCEPT

echo "saving"
iptables-save > /etc/iptables.rules
echo "done"
