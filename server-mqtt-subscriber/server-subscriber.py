import paho.mqtt.client as mqtt
import os
import re
import sys

OPERATION_ADD = 'A'
OPERATION_DELETE = 'D'


class Message:
    def __init__(self, message):
        if not self.is_valid_message(message):
            raise RuntimeError("The message was not valid")
        self.operation, self.mac_addr = message.split()

    @staticmethod
    def is_valid_message(msg):
        words = msg.split()
        if len(words) != 2:
            return False
        
        operation_regex = "^(A|R)"
        operation_regex_obj = re.compile(operation_regex)

        # courtesy of https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
        mac_regex = ("^([0-9A-Fa-f]{2}[:-])" +
                "{5}([0-9A-Fa-f]{2})")            
        mac_regex_obj = re.compile(mac_regex)

        if not re.search(operation_regex_obj, words[0]):
            return False
        if not re.search(mac_regex_obj, words[1]):
            return False

        return True


class MQTT_ACL_manager:
    def __init__(self, args):
        os.chdir("/home/maxm/Documents/seminar/server-mqtt-subscriber")
        client = mqtt.Client(protocol=mqtt.MQTTv5)
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(args[0], int(args[1]), 60)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()

    # reads the existing acl from the file, clears it, and then writes the new acl, 
    # which is the old acl with the specified operation applied to it
    # TODO: maybe make backup of old ACL in case something goes wrong while writing
    def handle_acl_update(self, msg):
        try: 
            msg = Message(msg.payload.decode("utf-8"))
        except RuntimeError as e:
            print("Error: {}".format(e))
            return

        with open("acl.txt", 'r+') as file:
            acl_set = self.construct_set_from_file(file)

            print(acl_set)
        
            if (msg.operation == OPERATION_ADD):
                acl_set.add(msg.mac_addr)
            elif (msg.operation == OPERATION_DELETE):
                acl_set.remove(msg.mac_addr)
            
            # clear the file
            file.truncate(0)

            file.write('\n'.join(acl_set))

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc, fifth_argument):
        if rc==0:
            print("Connected successfully")
        else:
            print("Connection attempt failed")

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("$SYS/#")
        client.subscribe("aclUpdate")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        if msg.topic == "aclUpdate":
            self.handle_acl_update(msg)

    # makes a set consisting of each line in file
    def construct_set_from_file(self, file):
        output_set = set()
        for line in file:
            output_set.add(line.strip('\x00\n')) # strip null- and newline chars before adding
        return output_set


if __name__ == "__main__":
    # TODO make a somewhat robust cli argument system
    if len(sys.argv) != 3:
        raise RuntimeError("Invalid number of arguments: please use ...")
    MQTT_ACL_manager(sys.argv[1:])
