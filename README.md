# seminar-intersct-project

## Deploy gateway (client)
1. Clone this repo.
2. Put your OpenVPN configuration file/certificate inside the "vagrant box" directory.
3. cd inside the "vagrant box" directory.
4. Edit line 6 of the file "Vagrantfile" to set an IP address for the VM, which will be used as the lab subnet router. See comment inside the file.
5. Edit line 9 of the file "Vagrantfile" to set the IP range of your LAN in CIDR notation. See comment inside the file.
6. Edit line 12 of the file "Vagrantfile" to set the network adapter you want to use for the lab subnet.
7. Edit line 15 of the file "Vagrantfile" to reflect the name of your OpenVPN config/certificate file. See comment inside the file.
8. Edit lines 16, 17 and 51 of file "iptables.sh" to use your LAN's IP and subnet mask. See the comments inside the file.
9. Configure the subnet you want to use for the lab in the file "dhcp_conf1".
10. Run "vagrant up".
