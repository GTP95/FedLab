#!/bin/python

import requests
import sys
import ipaddress
import os

token='e3df244fb16186e8aa071e0e430652dcebf6d821'
IP_RANGE=""


if len(sys.argv)!=2:
	print("Usage: "+ sys.argv[0] + " party_name")
	sys.exit()

partyName=sys.argv[1]
r=requests.get('http://131.155.69.149:8000/api/ipam/ip-ranges/', headers={'Authorization': 'Token '+token, 'Accept': 'application/json; indent=4'})
for ipRange in r.json()['results']:
	if ipRange['tenant']['slug']==partyName:
		IP_RANGE=ipRange['start_address']
		network=ipaddress.ip_network(ipRange['start_address'])
		netmask=str(network.netmask)
		subnetIP=str(network.network_address)
		iterator=network.hosts()
		firstIP=str(next(iterator))
		for ip in iterator:	#Look what I'm forced to do to get the last valid host IP address..
			lastIP=ip

lastIP=str(lastIP)

#Configure the DHCP server
os.system("sed -i '13s/192.168.5.0/"+subnetIP+"/'"+" dhcpd.conf")
os.system("sed -i '13s/255.255.255.0/"+netmask+"/'"+" dhcpd.conf")
os.system("sed -i '14s/192.168.5.2/"+firstIP+"/'"+" dhcpd.conf")
os.system("sed -i '14s/192.168.5.255/"+lastIP+"/'"+" dhcpd.conf")

#Configure iptables
os.system("sudo bash iptables.sh "+IP_RANGE)
