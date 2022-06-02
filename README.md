# FedLab

## Deploy gateway (client)
1. Clone this repo.
2. Put your OpenVPN configuration file/certificate inside the "vagrant box" directory.
3. cd inside the "vagrant box" directory.
4. Edit line 6 of the file "Vagrantfile" to set an IP address for the VM, which will be used as the lab subnet router. See comment inside the file.
5. Edit line 9 of the file "Vagrantfile" to set the IP range of your LAN in CIDR notation. See comment inside the file. Note: this is not the gateway subnet, but your own LAN.
6. Edit lines 12 and 15 of the file "Vagrantfile" to set the IP range of your subnet. This has to correspond with VM_IP. See comment inside the file.
7. Edit lines 19 and 20 of the file "Vagrantfile" to define the range in which the DHCP server of the gateway will distribute IP addresses. See comment inside the file.
8. Edit line 23 of the file "Vagrantfile" to set the network adapter you want to use for the lab subnet.
9. Edit line 26 of the file "Vagrantfile" to reflect the name of your OpenVPN config/certificate file. See comment inside the file.
10. Run `vagrant up`.

In order to connect multiple devices to the gateway, a switch or router in AP mode (with no NAT/DHCP) is supposed to be connected to the network adapter you chose in step 8.

Before applying any of the following operations, run `vagrant ssh` from the `vagrant box` directory to get a shell for the client. `$MAC_ADDR` represents the MAC address of the device you want to add to the ACL.

- **Add a device to the ACL**

    `sudo ./manage_acl.sh add $MAC_ADDR`

- **Remove a device from the ACL**

    `sudo ./manage_acl.sh remove $MAC_ADDR`
