#!/bin/bash

# Script for retrieving a manual from the FTP server

HOST=localhost
USER=intersect
PASSWORD=intersect

FILE=$1

ftp -pinv $HOST <<EOF
user $USER $PASSWORD
# cd /path/to/file
get $FILE
bye
EOF
