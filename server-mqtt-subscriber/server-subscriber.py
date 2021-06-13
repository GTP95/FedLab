import paho.mqtt.client as mqtt
import os
import re
import argparse

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
        
        operation_regex = "^(A|D)"
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

        client.connect(args.server, args.port, 60)

        # blocking call that keeps the client running by handling network traffic,
        # dispatching callbacks and reconnecting in case of disconnects
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

        acl_set = set()
        with open("acl.txt", 'r') as file:
            acl_set = self.construct_set_from_file(file)

        if (msg.operation == OPERATION_ADD):
            acl_set.add(msg.mac_addr)
        elif (msg.operation == OPERATION_DELETE):
            acl_set.discard(msg.mac_addr)

        with open("acl.txt", 'w') as file:
            # clear the file
            file.truncate(0)

            file.write('\n'.join(acl_set))

    # called when a CONNACK is received from the server, i.e. when a connection has been established
    def on_connect(self, client, userdata, flags, rc, fifth_argument):
        if rc==0:
            print("Connected successfully")
        else:
            print("Connection attempt failed")

        # by subscribing in on_connect(), we make sure that the subscription is
        # renewed when reconnected after a disconnect
        client.subscribe("aclUpdate")

    # called when a relevant PUB message is received from the broker
    def on_message(self, client, userdata, msg):
        # print(msg.topic+" "+str(msg.payload))
        # as long as the client only has the aclUpdate subscription, this check is redundant
        if msg.topic == "aclUpdate":
            self.handle_acl_update(msg)

    # makes a set consisting of each line in file
    def construct_set_from_file(self, file):
        output_set = set()
        for line in file:
            output_set.add(line.strip('\x00\n')) # strip null- and newline chars before adding
        return output_set


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MQTT subscriber for the INTERSCT Federated Lab server")

    parser.add_argument("-s", "--server", nargs=1, metavar="server_identifier", type=str, default="localhost",
        help="The identifier for the device on which the MQTT broker runs.\
            This may be a hostname (e.g. localhost), URL or IP address")

    parser.add_argument("-p", "--port", nargs=1, metavar="broker_port", type=int, default=1883,
        help="The port used by the MQTT broker")

    args = parser.parse_args()

    MQTT_ACL_manager(args)
