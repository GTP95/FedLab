# seminar-intersct-project

## Deploy
1. Clone this repo
2. Put your OpenVPN configuration file/certificate inside the "vagrant box" directory
3. Reserve a static IP on your LAN. It will be used for the gateway
4. cd inside the "vagrant box" directory
5. Edit line 4 of the file "Vagrantfile" to use the IP address you reserverd. See comment inside the file
6. Edit line 7 of the file "Vagrantfile" to reflect the name of your OpenVPN config/certificate file. See comment inside the file
7. Edit lines 17, 18 and 35 of file "iptables.sh" to use your LAN's IP and subnet mask. See the comments inside the file
8. Run "vagrant up"
9. If you have multiple network interfaces on your machine, Vagrant will ask you which one to bridge to. Choose one that is connected to the LAN 
where you will connect your IoT devices
10. Configure your IoT devices to use the IP you reserved as the defaut gateway's IP 
