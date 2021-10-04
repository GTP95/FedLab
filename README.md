# seminar-intersct-project

## Deploy gateway (client)
1. Clone this repo.
2. Put your OpenVPN configuration file/certificate inside the "vagrant box" directory.
3. cd inside the "vagrant box" directory.
4. Edit line 6 of the file "Vagrantfile" to set an IP address for the VM, which will be used as the lab subnet router. See comment inside the file.
5. Edit line 9 of the file "Vagrantfile" to set the network adapter you want to use for the lab subnet.
6. Edit line 12 of the file "Vagrantfile" to reflect the name of your OpenVPN config/certificate file. See comment inside the file.
7. Edit lines 16, 17 and 51 of file "iptables.sh" to use your LAN's IP and subnet mask. See the comments inside the file.
8. Configure the subnet you want to use for the lab in the file "dhcp_conf1".
9. Run "vagrant up".
