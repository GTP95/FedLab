#!/bin/bash

# Script for transferring a manual to the FTP server.
# The specified file with be prepended with the party nickname

HOST=localhost
USER=intersect
PASSWORD=intersect
# PARTY_NICKNAME=`cat /home/vagrant/partynickname.txt`
PARTY_NICKNAME=UT

FILE=$1

FILE_WITH_PARTY_PREFIX="${PARTY_NICKNAME}_${FILE}"

# make temp file because there appears to be no way to change the file name with the ftp put command
cp $1 $FILE_WITH_PARTY_PREFIX

ftp -pinv $HOST <<EOF
user $USER $PASSWORD
# cd /path/to/file
put $FILE_WITH_PARTY_PREFIX
bye
EOF

# delete the temp file
rm $FILE_WITH_PARTY_PREFIX
