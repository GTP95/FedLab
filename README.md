# FedLab

## Deploy the server (quick instructions)
1. Install Docker
2. Install docker-compose
3. Clone this repo
4. Initialize the configuration files and certificates for OpenVPN. Substitute `VPN.SERVERNAME.COM` with the static IP or URL of your server:
```BASH
docker-compose run --rm openvpn ovpn_genconfig -u udp://VPN.SERVERNAME.COM -p "route 192.168.201.0 255.255.255.0"
docker-compose run --rm openvpn ovpn_initpki
```
5. Start OpenVPN, Federated Lab Directory, and FTP server containers:
```BASH
docker-compose up -d
```
6. Clone the netbox-docker GitHub repository and cd into the directory that contains the repo:
```BASH
git clone -b release https://github.com/netbox-community/netbox-docker.git
cd netbox-docker
```
7. Create a new file called `docker-compose.override.yml` and paste inside the following:
```YAML
version: '3.4'
services:
  netbox:
    ports:
      - 8080
    networks:
      server_intersect_docker_network:
        ipv4_address: 192.168.201.9

  netbox-worker:
    networks:
      - server_intersect_docker_network

  netbox-housekeeping:
    networks:
      - server_intersect_docker_network

  postgres:
    networks:
      - server_intersect_docker_network

  redis:
    networks:
      - server_intersect_docker_network

  redis-cache:
    networks:
      - server_intersect_docker_network


networks:
  server_intersect_docker_network:
    external: true
```
8. run `docker-compose pull`
9. Run `docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d`

For more detailed instructions on how to deploy the server and how to operate it, refer to the server manual.

## Deploy Bundle Box (client, quick instructions)
1. Uncompress the archive containing the Bundle Box in a convenient location on your system.
2. Navigate to that location, enter the `Vagrant Box` directory and open the file `Vagrantfile`.
3. On line 4 of the Vagrantfile, substitute `nickname` with a nickname you wish to appear on the Federated Lab Directory as your party name
4. On line 7 of the Vagrantfile, substitute `<YOUR_LAB_SUBNET_ADAPTER>` with the name of the network interface you are using to connect your computer to WAN as it is called by the OS (i.e. the one you use to connect to internet, e.g. enp2s0 on a Linux system).
5. On line 10 of the Vagrantfile, substitute `<YOUR-IP-RANGE>` with the IP address of your LAN in CIDR notation, e.g. 192.168.0.0/24.
6. On line 19 of the Vagrantfile, substitute `<RESERVED_IP>` with the IP address you reserved on your LAN for the Bundle Box.
7. Run the command
```BASH
    vagrant up
```
to provision and start the Bundle Box.
    
For more deatiled instructions and for a description of how to operate a Bundle Box, refer to the user manual.

