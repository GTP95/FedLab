#!/bin/bash

# Script has to be run as sudo to modify arptables
if [ "$EUID" -ne 0 ]
  then echo "Please run the script as root (sudo blockAll.sh ...)"
  exit
fi

text="Are you sure you would like to run blockAll?"
text="$text This will block all incoming and outcoming traffic."
text="$text [y/n]"
read -p "$text" -n 1 -r
echo    # insert a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    arptables -P INPUT DROP
	arptables -P OUTPUT DROP
	arptables -P FORWARD DROP
else
	echo "Nothing done"
fi


