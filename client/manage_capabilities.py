# Example of the format:
# {
#   'capabilities': [
#     {
#       "device": "192.168.5.58",  // use only a plain text name here or MAC / another ID?
#       "port": "1024",
#       "capability_name": "very cool hack",
#       "capability_id": "9f96d940-ea30-472e-99d5-d2dc9f45bbba",  // just a UUID, or maybe we can hash some data of the capability?
#       "description": "hack that destroys space and time"
#     },
#     {
#       "device": "192.168.5.231",  // use only a plain text name here or MAC / another ID?
#       "port": "1028",
#       "capability_name": "monitor voice commands",
#       "capability_id": "9f96d940-ea30-472e-99d5-d2dc9f45bbbb",  // just a UUID, or maybe we can hash some data of the capability?
#       "description": "monitor voice commands to invade people's privacy (get permission first pls)"
#     }
#   ]
# }

import json
import os
from rules_and_port_generator import generatePortAndAddRules


# 2 weeks
TTL = 14*24*60*60
SERVER = "10.0.2.2"
PORT = 1883
partyNickname = ""
GATEWAY_IP = ""

# Get the gateway ip from the dhcpd.conf file
file = open("/etc/dhcp/dhcpd.conf", "r")
for line in file:
    if " option routers" in line:
        GATEWAY_IP = line[17:-2]
file.close()

# Get the party nickname
f = open("/home/vagrant/partynickname.txt", "r")
partyNickname = f.readline()
f.close


class MqttCapabilityUpdateManager:
    def publish_capability_add(self, capability_string):
        # use MQTT-CLI to publish the message
        os.system("mqtt pub -h {} -t capability_add -m '{}'".format(SERVER, capability_string))
        # print("\nmqtt pub -h {} -t capability_add -m '{}'\n".format(
        #    SERVER,
        #    capability_string
        #))


mqtt_client = MqttCapabilityUpdateManager()


def read_directory():
    if not os.path.exists("local_capability_directory"):
        construct_empty_directory()

    with open("local_capability_directory", 'r') as f:
        result = json.load(f)

    return result


def write_directory(cap_directory):
    with open("local_capability_directory", 'w') as f:
        f.write(json.dumps(cap_directory))


def pretty_print_directory():
    with open("local_capability_directory", 'r') as f:
        result = json.load(f)
        print(json.dumps(result, indent=2))


def construct_empty_directory():
    with open("local_capability_directory", 'w') as f:
        f.write(json.dumps({"capabilities": []}))


def construct_local_capability_object(ip, gateway_port, device_port, name, desc):
    return {
           "device": ip,
           "gateway_port": gateway_port,
           "device_port": device_port,
           "capability_name": name,
           "description": desc,
           "is_capability": True
         }


def construct_remote_capability_object(name, desc, port):
    return {
           "party_name": partyNickname,
           "gateway_ip": GATEWAY_IP,
           "gateway_port": port,
           "capability_name": name,
           "description": desc,
           "is_capability": True
         }


def construct_local_device_object(device_ip, name, desc):
    return {
           "device": device_ip,
           "gateway_port": None,
           "device_port": None,
           "capability_name": name,
           "description": desc,
           "is_capability": False
         }


def construct_remote_device_object(device_ip, name, desc):
    return {
           "party_name": partyNickname,
           "gateway_ip": device_ip,
           "gateway_port": None,
           "capability_name": name,
           "description": desc,
           "is_capability": False
         }


def add_capability(ip, device_port, name, desc):
    cap_directory = read_directory()

    gateway_port = generatePortAndAddRules(ip, device_port)

    new_capability = construct_local_capability_object(
        ip, str(gateway_port), device_port, name, desc)
    cap_directory["capabilities"].append(new_capability)

    remote_capability = construct_remote_capability_object(
        name, desc, str(gateway_port))
    mqtt_client.publish_capability_add(
        json.dumps(remote_capability, indent=2))

    write_directory(cap_directory)


def remove_capability(uuid):
    # TODO: fix this, since ID is no longer there

    # cap_directory = read_directory()
    # print(cap_directory['capabilities'])
    #
    # # only keep items that do not have the specified UUID
    # cap_directory['capabilities'] = list(filter(
    #     lambda x: x["capability_id"] != uuid,
    #     cap_directory['capabilities'])
    # )
    #
    # mqtt_client.publish_capability_update("remove", uuid)
    #
    # write_directory(cap_directory)
    pass


def add_device(ip, name, desc):
    cap_directory = read_directory()

    new_device = construct_local_device_object(
        ip, name, desc)
    cap_directory["capabilities"].append(new_device)

    remote_device = construct_remote_device_object(
        ip, name, desc)
    mqtt_client.publish_capability_add(
        json.dumps(remote_device, indent=2))

    write_directory(cap_directory)


def remove_device():
    # TODO
    pass
