#!/bin/python
import os

try:
  file=open('MAC_addresses', 'r')

  for line in file:
    tmpList=line.split()  #splits line after space
    macAddress=tmpList[1]
    os.system("arptables -A OUTPUT --destination-mac " + macAddress + " -j ACCEPT")
    os.system("arptables -A INPUT --source-mac " + macAddress + " -j ACCEPT")
  file.close()

except FileNotFoundError as e:
  print("Can't find the file to restore ACL's rules, exiting")
