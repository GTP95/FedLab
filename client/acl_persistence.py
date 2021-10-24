#!/bin/python
import os

try:
	file=open('MAC_addresses', 'r')

	for macAddress in file:
		macAddress.strip()	#removes newline
		os.system("arptables -A OUTPUT --destination-mac " + macAddress + " -j ACCEPT")
		os.system("arptables -A INPUT --source-mac" + macAddress + " -j ACCEPT")
	file.close()

except FileNotFoundError as e:
	print("Can't find the file to restore ACL's rules, exiting")

