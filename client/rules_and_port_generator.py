#!/bin/python

from contextlib import closing
import socket
import os
import sys
import random


def isAvailable(port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        res = sock.connect_ex(('localhost', port))
        if res == 0:
            return False
        else:
            return True


def generatePort():
	for port in range(1024, 65535+1):
		if isAvailable(port):
			return port


def addIptablesRules(ipAddress, devicePort, externalPort):
	os.system("iptables -t nat -A PREROUTING -p tcp --dport " + str(externalPort)
	          + " -j DNAT --to-destination " + str(ipAddress) + ":" + str(devicePort))
	os.system("iptables -t nat -A POSTROUTING -p tcp --dport "
	          + str(devicePort) + " -j SNAT --to-source " + str(ipAddress))
	#Note: assuming that "echo 1 > /proc/sys/net/ipv4/ip_forward" and "/proc/sys/net/ipv4/conf/eth0/forwarding" do basically the same so not enabling
	#forwarding here as already enabled in Vagrantfile with "echo 1 > /proc/sys/net/ipv4/ip_forward"


def generatePortAndAddRules(deviceIpAddress, devicePort):
	if not os.geteuid() == 0:
		sys.exit('Error: this script must be run as root')
	externalPort = generatePort()
	addIptablesRules(deviceIpAddress, devicePort, externalPort)
	return externalPort
