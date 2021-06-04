import paho.mqtt.client as mqtt
import os
import re


def is_valid_message(msg):
    words = msg.split()
    if len(words) != 2:
        return False
    
    operation_regex = "^(A|D)"
    operation_regex_obj = re.compile(operation_regex)

    # Regex to check valid MAC address (courtesy of https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/)
    mac_regex = ("^([0-9A-Fa-f]{2}[:-])" +
             "{5}([0-9A-Fa-f]{2})")            
    mac_regex_obj = re.compile(mac_regex)

    if not re.search(operation_regex_obj, words[0]):
        return False
    if not re.search(mac_regex_obj, words[1]):
        return False

    return True


# reads the existing acl from the file, clears it, and then writes the new acl, 
# which is the old acl with the specified operation applied to it
# TODO: maybe make backup of old ACL in case something goes wrong while writing
def handle_acl_update(msg):
    decoded_msg = msg.payload.decode("utf-8")
    if not is_valid_message(decoded_msg):
        return

    with open("acl.txt", 'r+') as file:
        acl_set = set()
        for line in file:
            acl_set.add(line)
        
        # clear the file
        file.truncate(0)
        
        acl_set.add(decoded_msg)
        
        file.write('\n'.join(acl_set))


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc, fifth_argument):
    if rc==0:
        print("Connected successfully")
    else:
        print("Connection attempt failed")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe("aclUpdate")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "aclUpdate":
        handle_acl_update(msg)


os.chdir("/home/maxm/Documents/seminar/server-mqtt-subscriber")
client = mqtt.Client(protocol=mqtt.MQTTv5)
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
