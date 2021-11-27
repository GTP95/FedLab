import paho.mqtt.client as mqtt
import os
import re
import argparse

OPERATION_ADD = 'A'
OPERATION_DELETE = 'D'


class DeviceDirectoryEntry:
    def __init__(self, mac_addr, status):
        if not self.is_valid_update(mac_addr, status):
            raise RuntimeError("Invalid device directory update")
        self.mac_addr, self.status = mac_addr, status

    def __str__(self):
        return "{} {}".format(self.mac_addr, self.status)

    @classmethod
    def from_str(cls, entry: str) -> 'Book':
        if not DeviceDirectoryEntry.is_valid_entry(entry):
            raise RuntimeError("Malformed line detected in device_directory")
        words = entry.split()
        return cls(mac_addr=words[0], status=words[1])

    @staticmethod
    def is_valid_entry(line):
        words = line.split()
        if len(words) != 2:
            return False

        # courtesy of https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
        mac_regex = ("^([0-9A-Fa-f]{2}[:-])"
                     + "{5}([0-9A-Fa-f]{2})")
        mac_regex_obj = re.compile(mac_regex)

        status_regex = "^(online|offline)$"
        status_regex_obj = re.compile(status_regex)

        if not re.search(mac_regex_obj, words[0]):
            return False
        if not re.search(status_regex_obj, words[1]):
            return False

        return True

    @staticmethod
    def is_valid_update(mac_addr, status):
        # courtesy of https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
        mac_regex = ("^([0-9A-Fa-f]{2}[:-])"
                     + "{5}([0-9A-Fa-f]{2})")
        mac_regex_obj = re.compile(mac_regex)

        status_regex = "^(online|offline)$"
        status_regex_obj = re.compile(status_regex)

        if not re.search(mac_regex_obj, mac_addr):
            return False
        if not re.search(status_regex_obj, status):
            return False

        return True


class AddRemoveMessage:
    def __init__(self, message):
        if not self.is_valid_message(message):
            raise RuntimeError("The add/remove message was not valid")
        self.operation, self.mac_addr = message.split()

    @staticmethod
    def is_valid_message(msg):
        words = msg.split()
        if len(words) != 2:
            return False

        operation_regex = "^(A|D)"
        operation_regex_obj = re.compile(operation_regex)

        # courtesy of https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
        mac_regex = ("^([0-9A-Fa-f]{2}[:-])"
                     + "{5}([0-9A-Fa-f]{2})")
        mac_regex_obj = re.compile(mac_regex)

        if not re.search(operation_regex_obj, words[0]):
            return False
        if not re.search(mac_regex_obj, words[1]):
            return False

        return True


class DeviceStatusMessage:
    def __init__(self, message):
        if not self.is_valid_message(message):
            raise RuntimeError("The device status message was not valid")
        self.mac_addr, self.status = message.split()

    @staticmethod
    def is_valid_message(msg):
        words = msg.split()
        if len(words) != 2:
            return False

        # courtesy of https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
        mac_regex = ("^([0-9A-Fa-f]{2}[:-])"
                     + "{5}([0-9A-Fa-f]{2})")
        mac_regex_obj = re.compile(mac_regex)

        status_regex = "^(online|offline)$"
        status_regex_obj = re.compile(status_regex)

        if not re.search(mac_regex_obj, words[0]):
            return False
        if not re.search(status_regex_obj, words[1]):
            return False

        return True


class MqttAclManager:
    def __init__(self, args):
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
        init_file_if_not_exists()

        try:
            msg = AddRemoveMessage(msg.payload.decode("utf-8"))
        except RuntimeError as e:
            print("Error: {}".format(e))
            return

        device_directory = dict[str, DeviceDirectoryEntry]()
        with open("device_directory", 'r') as file:
            device_directory = self.construct_dict_from_file(file)

        if (msg.operation == OPERATION_ADD):
            device_directory[msg.mac_addr] = DeviceDirectoryEntry(
                msg.mac_addr, "offline")
        elif (msg.operation == OPERATION_DELETE):
            del device_directory[msg.mac_addr]

        suffix = '\n' if len(device_directory) > 0 else ''
        with open("device_directory", 'w') as file:
            file.write(
                '\n'.join(map(lambda x: str(x), device_directory.values())) + suffix)

    def handle_capability_add(self, msg):
        init_file_if_not_exists()

        # TODO: some validation

        with open("device_directory", 'a') as file:
            file.writelines(msg.payload.decode("utf-8") + '\n')

    def handle_device_status_update(self, msg):
        init_file_if_not_exists()

        try:
            msg = DeviceStatusMessage(msg.payload.decode("utf-8"))
        except RuntimeError as e:
            print("Error: {}".format(e))
            return

        device_directory = dict[str, DeviceDirectoryEntry]()
        with open("device_directory", 'r') as file:
            device_directory = self.construct_dict_from_file(file)

        if msg.mac_addr not in device_directory:
            print("Error: There was an error indexing the device")
            return

        if (msg.status == "online"):
            device_directory[msg.mac_addr].status = "online"
        elif (msg.status == "offline"):
            device_directory[msg.mac_addr].status = "offline"

        suffix = '\n' if len(device_directory) > 0 else ''
        with open("device_directory", 'w') as file:
            file.write(
                '\n'.join(map(lambda x: str(x), device_directory.values())) + suffix)

    # called when a CONNACK is received from the server, i.e. when a connection has been established
    def on_connect(self, client, userdata, flags, rc, fifth_argument):
        if rc == 0:
            print("Connected successfully")
        else:
            print("Connection attempt failed")

        # by subscribing in on_connect(), we make sure that the subscription is
        # renewed when reconnected after a disconnect
        client.subscribe("aclUpdate")
        client.subscribe("device_status_update")
        client.subscribe("capability_add")

    # called when a relevant PUB message is received from the broker
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

        if msg.topic == "aclUpdate":
            self.handle_acl_update(msg)

        if msg.topic == "device_status_update":
            self.handle_device_status_update(msg)

        if msg.topic == "capability_add":
            self.handle_capability_add(msg)

    # makes a set consisting of each line in file
    def construct_dict_from_file(self, file):
        output_dict = dict[str, DeviceDirectoryEntry]()

        for line in file:
            try:
                entry = DeviceDirectoryEntry.from_str(line.strip('\n'))
                output_dict[entry.mac_addr] = entry
            except RuntimeError as e:
                print("Error: {}".format(e))

        return output_dict


def init_file_if_not_exists():
    if not os.path.exists("device_directory"):
        open("device_directory", 'w').close()


if __name__ == "__main__":
    path, _ = os.path.split(os.path.realpath(__file__))
    os.chdir(path)

    init_file_if_not_exists()

    parser = argparse.ArgumentParser(
        description="MQTT subscriber for the INTERSCT Federated Lab server")

    parser.add_argument("-s", "--server", metavar="server_identifier", type=str, default="localhost",
                        help="The identifier for the device on which the MQTT broker runs.\
            This may be a hostname, URL or IP address (defaults to localhost)")

    parser.add_argument("-p", "--port", metavar="broker_port", type=int, default=1883,
                        help="The port used by the MQTT broker (defaults to 1883)")

    args = parser.parse_args()

    MqttAclManager(args)
