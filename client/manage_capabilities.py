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
import requests
import re
import uuid

SERVER = "http://192.168.201.3:8080"
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
f.close()

def get_directory():
    resp = requests.get("{}/directory".format(SERVER))

    return "{}".format(resp.text)


def get_capabilities():
    resp = requests.get("{}/capabilities".format(SERVER))

    # return body
    return resp.content


def post_capability(capability_object):
    resp = requests.post("{}/capabilities".format(SERVER), json = capability_object)

    if (resp.status_code == 200):
        print("Capability was successfully posted to the directory.")
    else:
        print("Posting a capability to the directory failed with status code {}".format(resp.status_code))


def remote_remove_capability(remote_remove_capability_object):
    resp = requests.post("{}/removeCapabilityRequest".format(SERVER), json = remote_remove_capability_object)

    if (resp.status_code == 200):
        print("Capability was successfully removed from the directory.")
    else:
        print("Removing a capability from the directory failed with status code {}".format(resp.status_code))


def get_devices():
    resp = requests.get("{}/devices".format(SERVER))

    # return body
    return resp.content


def post_device(device_object):
    resp = requests.post("{}/devices".format(SERVER), json = device_object)

    if (resp.status_code == 200):
        print("Device was successfully posted to the directory.")
    else:
        print("Posting a device to the directory failed with status code {}".format(resp.status_code))


def remote_remove_device(remove_device_object):
    resp = requests.post("{}/removeDeviceRequest".format(SERVER), json = remove_device_object)

    if (resp.status_code == 200):
        print("Device was successfully removed from the directory.")
    else:
        print("Removing a device from the directory failed with status code {}".format(resp.status_code))


def device_status_update(device_status_update):
    resp = requests.post("{}//statusUpdate".format(SERVER), json = device_status_update)


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


def construct_local_capability_object(ip, device_port, name, desc, uuid):
    return {
        "device": ip,
        "device_port": device_port,
        "capability_name": name,
        "description": desc,
        "is_capability": True,
        "uuid": uuid
    }


def construct_remote_capability_object(device_ip, port, name, desc, uuid):
    return {
        "party_name": partyNickname,
        "gateway_ip": device_ip,
        "gateway_port": port,
        "capability_name": name,
        "description": desc,
        "is_capability": True,
        "uuid": uuid
    }


def construct_local_device_object(device_ip, name, desc):
    return {
        "device": device_ip,
        "device_port": None,
        "capability_name": name,
        "description": desc,
        "is_capability": False
    }


def construct_remote_remove_capability_object(uuid):
    return  {
        "identifier": uuid
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


def construct_remove_device_object(device_ip):
    return  {
        "identifier": device_ip
    }


def add_capability(ip, device_port, name, desc):
    cap_directory = read_directory()

    capability_uuid = str(uuid.uuid4())
    new_capability = construct_local_capability_object(
        ip, device_port, name, desc, capability_uuid)
    cap_directory["capabilities"].append(new_capability)

    remote_capability_object = construct_remote_capability_object(
        ip, device_port, name, desc, capability_uuid)
    post_capability(remote_capability_object)

    add_capability_rules(ip, device_port)

    write_directory(cap_directory)


def remove_capability(uuid):
    remote_remove_capability(construct_remote_remove_capability_object(uuid))
    # TODO do more stuff
    pass


def check_args(mac, name, desc, expose):
    if expose:
        if name is None or desc is None:
            print("-n and -d are required with the -e flag")
            return

    mac = (mac.replace("-", ":")).lower()
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac):
        add_device(mac, name, desc, expose)
    else:
        print("MAC address is invalid")


def expose_device(ip, name, desc):
    cap_directory = read_directory()

    new_device = construct_local_device_object(
        ip, name, desc)
    cap_directory["capabilities"].append(new_device)

    remote_device_object = construct_remote_device_object(
        ip, name, desc)
    post_device(remote_device_object)

    add_device_rule(ip)

    write_directory(cap_directory)


def add_device(mac, name, desc, expose):
    os.system("sudo ./manage_acl.sh add {}".format(mac))

    if expose:
        ip=""
        file = open("./MAC_addresses", "r")
        for line in file:
            if mac in line:
                ip="".join(line.split(" ", 1)[:-1])
        file.close()
        if ip == "":
            os.system("echo 'Device was not added to the acl'")
        expose_device(ip, name, desc)


def remove_device(device_ip):
    remote_remove_device(construct_remove_device_object(device_ip))
    # TODO do more stuff
    pass


def add_capability_rules(device_ip, device_port):
    os.system("sudo iptables -A FORWARD -i tun0 -d {} -p tcp --dport {} -j ACCEPT".
              format(device_ip, device_port))
    os.system("sudo iptables -A FORWARD -i tun0 -d {} -p udp --dport {} -j ACCEPT".
              format(device_ip, device_port))


def add_device_rule(device_ip):
    os.system("sudo iptables -A FORWARD -i tun0 -d {} -j ACCEPT".format(device_ip))
