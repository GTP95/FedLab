#!/bin/python

from contextlib import closing
import socket
import os
import sys
import subprocess
import random
from netifaces import interfaces, ifaddresses, AF_INET


def isAvailable(port):

    #check if port appears in iptables' NAT table
    listNATrules="sudo iptables -t nat -L" 
    result = subprocess.check_output(listNATrules, shell=True)
    if not str(result).find(str(port)) == -1:
        return False       

    #check if port is in use at this moment
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        res = sock.connect_ex(('localhost', port))  
        if res == 0:
            return False

    return True

def generatePort():
    isValid=False
    while(not isValid):
    	port=random.randrange(1024, 65535+1)	    
    	if isAvailable(port):
            isValid=True
    return port


def addIptablesRules(ipAddress, devicePort, externalPort):
	address=ifaddresses('enp0s8')[AF_INET][0]['addr']	#get gateway's internal address	
	os.system("sudo iptables -t nat -A PREROUTING -p tcp --dport " + str(externalPort)
	          + " -j DNAT --to-destination " + str(ipAddress) + ":" + str(devicePort))
	os.system("sudo iptables -t nat -A POSTROUTING -p tcp --dport "
	          + str(devicePort) + " -j SNAT --to-source " + address)
	#Note: assuming that "echo 1 > /proc/sys/net/ipv4/ip_forward" and "/proc/sys/net/ipv4/conf/eth0/forwarding" do basically the same so not enabling
	#forwarding here as already enabled in Vagrantfile with "echo 1 > /proc/sys/net/ipv4/ip_forward"


def generatePortAndAddRules(deviceIpAddress, devicePort):
	externalPort = generatePort()
	addIptablesRules(deviceIpAddress, devicePort, externalPort)
	return externalPort
