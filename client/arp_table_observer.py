import time
import os
import time
import re
from watchdog.observers import Observer
from watchdog.events import *
import math
import paho.mqtt.client as mqtt

# 2 weeks
TTL = 14*24*60*60
SERVER = "localhost"
PORT = 1883

class AclEntry:
    def __init__(self, entry):
        if not self.is_valid_entry(entry):
            raise RuntimeError("The ACL entry was not valid: " + entry)
        self.mac_addr, self.last_used, self.status = entry.split()
        self.last_used = int(self.last_used)

    def __str__(self):
        return "{} {} {}".format(self.mac_addr, self.last_used, self.status)

    @staticmethod
    def is_valid_entry(line):
        words = line.split()
        if len(words) != 3:
            return False

        # courtesy of https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
        mac_regex = ("^([0-9A-Fa-f]{2}[:-])" +
                "{5}([0-9A-Fa-f]{2})")            
        mac_regex_obj = re.compile(mac_regex)

        number_regex = "^\d+$"
        number_regex_obj = re.compile(number_regex)

        status_regex = "^(online|offline)$"
        status_regex_obj = re.compile(status_regex)

        if not re.search(mac_regex_obj, words[0]):
            return False
        if not re.search(number_regex_obj, words[1]):
            return False
        if not re.search(status_regex_obj, words[2]):
            return False

        return True


class ArpChangeHandler(FileSystemEventHandler):

    # def __init__(self) -> None:
    #     super().__init__()
        # self.previous_call = time.time()
    
    def on_modified(self, event):
        if event.is_directory:
            return

        # if time.time() - self.previous_call > 30:
        #     self.previous_call = time.time()
        #     return

        init_files_if_not_exists()

        current_time = math.floor(time.time())

        # store the MAC addresses in the ARP table in a list
        arp_table_mac_list = []
        with open('/proc/net/arp', 'r') as file:
            for line in file:
                for word in line.split():
                    # courtesy of https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
                    mac_regex = ("^([0-9A-Fa-f]{2}[:-])" +
                            "{5}([0-9A-Fa-f]{2})")            
                    mac_regex_obj = re.compile(mac_regex)

                    if re.search(mac_regex_obj, word):
                        arp_table_mac_list.append(word)

        acl = dict[str, AclEntry]()
        with open("MAC_addresses", 'r') as file:
            for line in file:
                try: 
                    entry = AclEntry(line.strip('\n'))
                    acl[entry.mac_addr] = entry
                except RuntimeError as e:
                    print("Error: {}".format(e))
                    return

        # determine whether entries in 'MAC_addresses' are to be refreshed or removed
        for mac_addr in acl.keys():
            # If a registered MAC address was found in the ARP table, update its time.
            # If the device was offline before, an update will be sent to the server.
            if acl[mac_addr].mac_addr in arp_table_mac_list:
                acl[mac_addr].last_used = current_time
                if entry.status == "offline":
                    acl[mac_addr].status = "online"
                    mqtt_client.publish_device_update(acl[mac_addr].mac_addr, "online")

            # If a registered MAC address was not found in the ARP table and
            # has not been connected for at least TTL seconds, remove it from the list.
            elif acl[mac_addr].last_used + TTL < current_time:
                del acl[mac_addr]
                os.system("sudo manage_acl.sh remove {}".format(mac_addr))

            # MAC address was not in found in the ARP table, but has not yet expired
            # If the device was online before, an update will be sent to the server.
            else:
                if acl[mac_addr].status == "online":
                    acl[mac_addr].status = "offline"
                    mqtt_client.publish_device_update(acl[mac_addr].mac_addr, "offline")


        suffix = '\n' if len(acl) > 0 else ''
        with open("MAC_addresses", 'w') as file:
            file.write('\n'.join(map(lambda x: str(x), acl.values())) + suffix)


class MqttDeviceStatusManager:
    def __init__(self):
        self.client = mqtt.Client(protocol=mqtt.MQTTv5)
        self.client.on_connect = self.on_connect

        self.client.connect(SERVER, PORT, 60)

    # called when a CONNACK is received from the server, i.e. when a connection has been established
    def on_connect(self, client, userdata, flags, rc, fifth_argument):
        if rc==0:
            print("Connected successfully")
        else:
            print("Connection attempt failed")

    def publish_device_update(self, mac_addr, status):
        message = "device_status_update", "{} {}".format(mac_addr, status)
        print("publishing message: {}".format(message))
        self.client.publish("device_status_update", "{} {}".format(mac_addr, status))


mqtt_client = MqttDeviceStatusManager()

def init_files_if_not_exists():
    if not os.path.exists("/tmp/arp_table"):
        open("/tmp/arp_table", 'w').close()

    if not os.path.exists("MAC_addresses"):
        open("MAC_addresses", 'w').close()


if __name__ == "__main__":
    path, _ = os.path.split(os.path.realpath(__file__))
    os.chdir(path)

    init_files_if_not_exists()

    observer = Observer()
    observer.schedule(ArpChangeHandler(), path="/tmp/arp_table", recursive=False) # monitoring /proc/net/arp does not work!
    observer.start()

    try:
        while True:
            # keep alive
            time.sleep(1)
        else:
            print("got it")
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
