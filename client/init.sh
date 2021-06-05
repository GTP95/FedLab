#!/bin/bash

# Script has to be run as sudo to modify arptables
if [ "$EUID" -ne 0 ]
  then echo "Please run the script as root (sudo init.sh ...)"
  exit
fi

MAC="$1"
ROUTER="${MAC//-/:}"

arptables -A OUTPUT --source-mac $ROUTER -j ACCEPT
arptables -A INPUT --destination-mac $ROUTER -j ACCEPT
