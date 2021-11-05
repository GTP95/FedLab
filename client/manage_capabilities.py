#!/usr/bin/python

# To run: sudo manage_capabilities.sh add/remove <MAC_ADDR> <PORT> <CAPABILITY_NAME> <CAPABILITY_DESC>

# Example of the format:
# {
#   'capabilities': [
#     {
#       "device": "11:22:33:44:55:66",  // use only a plain text name here or MAC / another ID?
#       "capability_name": "very cool hack",
#       "capability_id": "9f96d940-ea30-472e-99d5-d2dc9f45bbba",  // just a UUID, or maybe we can hash some data of the capability?
#       "description": "hack that destroys space and time"
#     },
#     {
#       "device": "22:33:44:55:66:77",  // use only a plain text name here or MAC / another ID?
#       "capability_name": "monitor voice commands",
#       "capability_id": "9f96d940-ea30-472e-99d5-d2dc9f45bbbb",  // just a UUID, or maybe we can hash some data of the capability?
#       "description": "monitor voice commands to invade people's privacy (get permission first pls)"
#     }
#   ]
# }

import json
import os
import uuid
import argparse


# 2 weeks
TTL = 14*24*60*60
SERVER = "10.0.2.2"
PORT = 1883
OPENVPN_CLIENT_NAME = "INTERSECT2" # configure this


class MqttCapabilityUpdateManager:
    def publish_capability_update(self, operation, capability_string):
        # use MQTT-CLI to publish the message
        # os.system("mqtt pub -h {} -t capability_update -m '{} {}'".format(SERVER, operation, capability_string))
        # print("mqtt pub -h {} -t capability_update -m '{} {}'".format(SERVER, operation, capability_string))
        pass


mqtt_client = MqttCapabilityUpdateManager()


def read_directory():
    if not os.path.exists("local_capability_directory"):
        construct_empty_directory()

    with open("local_capability_directory", 'r') as f:
        result = json.load(f)

    return result


def write_directory(cap_directory_json):
    with open("local_capability_directory", 'w') as f:
        f.write(cap_directory_json)


def pretty_print_directory():
    with open("local_capability_directory", 'r') as f:
        result = json.load(f)
        print(json.dumps(result, indent=2))


# for retrieving the OpenVPN client name of the bundle box
def get_client_name():



def construct_empty_directory():
    with open("local_capability_directory", 'w') as f:
        f.write(json.dumps({ "capabilities": [] }))


def construct_local_capability_object(mac, name, desc):
    return {
           "device": mac,
           "capability_name": name,
           "capability_id": str(uuid.uuid4()),
           "description": desc
         }


def construct_remote_capability_object(mac, name, desc):
    return {
           "party_name": OPENVPN_CLIENT_NAME,
           "device": mac,
           "capability_name": name,
           "capability_id": str(uuid.uuid4()),
           "description": desc
         }


def add_capability(mac, name, desc):
    cap_directory = read_directory()

    new_capability = construct_local_capability_object(mac, name, desc)
    cap_directory["capabilities"].append(new_capability)

    remote_capability = construct_remote_capability_object(mac, name, desc)
    mqtt_client.publish_capability_update("add", json.dumps(remote_capability))

    cap_directory_json = json.dumps(cap_directory)
    write_directory(cap_directory_json)


def remove_capability(mac, name, desc):
    cap_directory = read_directory()

    # TODO: not yet implemented


# if __name__ == "__main__":
#     path, _ = os.path.split(os.path.realpath(__file__))
#     os.chdir(path)
#
#     parser = argparse.ArgumentParser(description="Utility to manage the capabilities exposed by this bundle box.")
#
#     parser.add_argument("-m", "--mac", metavar="mac_addr", type=str, required=True,
#         help="The MAC address of the device for which you want to add a capability.")
#
#     parser.add_argument("-n", "--name", metavar="capability_name", type=str, required=True,
#         help="The name of the capability as it will show up in the capability directory")
#
#     parser.add_argument("-d", "--description", metavar="capability_desc", type=str, required=True,
#         help="The description of the capability as it will show up in the capability directory")
#
#     args = parser.parse_args()
#
#     add_capability(args.mac, args.name, args.description)
#     pretty_print_directory()
