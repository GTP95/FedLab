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


# 2 weeks
TTL = 14*24*60*60
SERVER = "10.0.2.2"
PORT = 1883
OPENVPN_CLIENT_NAME = "INTERSECT2"  # configure this


class MqttCapabilityUpdateManager:
    def publish_capability_update(self, operation, capability_string):
        # use MQTT-CLI to publish the message
        # os.system("mqtt pub -h {} -t capability_update -m '{} {}'".format(SERVER, operation, capability_string))
        print("\nmqtt pub -h {} -t capability_update -m '{} {}'\n".format(
            SERVER,
            operation,
            capability_string
        ))


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

    write_directory(cap_directory)


def remove_capability(uuid):
    cap_directory = read_directory()
    print(cap_directory['capabilities'])

    # only keep items that do not have the specified UUID
    cap_directory['capabilities'] = list(filter(
        lambda x: x["capability_id"] != uuid,
        cap_directory['capabilities'])
    )

    mqtt_client.publish_capability_update("remove", uuid)

    write_directory(cap_directory)
