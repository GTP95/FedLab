#!/bin/python

from contextlib import closing
import socket
import os
import sys
import subprocess
import random
from netifaces import interfaces, ifaddresses, AF_INET


def isAvailable(port):

    # check if port appears in iptables' NAT table
    listNATrules = "sudo iptables -t nat -L"
    result = subprocess.check_output(listNATrules, shell=True)
    if not str(result).find(str(port)) == -1:
        return False

    # check if port is in use at this moment
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        res = sock.connect_ex(('localhost', port))
        if res == 0:
            return False

    return True


def generatePort():
    isValid = False
    while(not isValid):
        port = random.randrange(1024, 65535+1)
        if isAvailable(port):
            isValid = True
    return port


def add_capability_rule(device_ip, device_port):
    os.system("sudo iptables -A FORWARD -d {} -p {} -j ACCEPT".format(
        device_ip, device_port))


def add_device_rule(device_ip):
    os.system("sudo iptables -A FORWARD -d {} -j ACCEPT".format(device_ip))


def addIptablesRules(ipAddress, devicePort, externalPort):
    # get gateway's internal address
    address = ifaddresses('enp0s8')[AF_INET][0]['addr']
    os.system(
        "sudo iptables -A FORWARD -d {} -p {} -j ACCEPT".format(ipAddress, devicePort))
    os.system("sudo iptables -t nat -A PREROUTING -p tcp --dport " + str(externalPort)
              + " -j DNAT --to-destination " + str(ipAddress) + ":" + str(devicePort))
    os.system("sudo iptables -t nat -A POSTROUTING -p tcp --dport "
              + str(devicePort) + " -j SNAT --to-source " + address)
    #Note: assuming that "echo 1 > /proc/sys/net/ipv4/ip_forward" and "/proc/sys/net/ipv4/conf/eth0/forwarding" do basically the same so not enabling
    #forwarding here as already enabled in Vagrantfile with "echo 1 > /proc/sys/net/ipv4/ip_forward"
