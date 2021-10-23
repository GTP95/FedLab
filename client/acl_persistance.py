#!/bin/python
import os

file=open('MAC_addresses', 'r')
macAddresses=file.readLines()

for macAddress in macAddresses:
	macAddress.strip()	#removes newline
	os.system("arptables -A OUTPUT --destination-mac " + macAddress + " -j ACCEPT")
	os.system("arptables -A INPUT --source-mac" + macAddress + " -j ACCEPT")
	
