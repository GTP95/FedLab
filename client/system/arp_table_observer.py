import time
import os
import time
import re
from watchdog.observers import Observer
from watchdog.events import *
import math
import manage_capabilities

# 2 weeks
TTL = 14*24*60*60


class AclEntry:
    def __init__(self, entry):
        if not self.is_valid_entry(entry):
            raise RuntimeError("The ACL entry was not valid: " + entry)
        self.ip, self.mac_addr, self.last_used, self.status = entry.split()
        self.last_used = int(self.last_used)

    def __str__(self):
        return "{} {} {} {}".format(self.ip, self.mac_addr, self.last_used, self.status)

    @staticmethod
    def is_valid_entry(line):
        words = line.split()
        if len(words) != 4:
            return False

        ip_regex = r'[0-9]+(?:\.[0-9]+){3}'
        ip_regex_obj = re.compile(ip_regex)

        # courtesy of https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
        mac_regex = ("^([0-9A-Fa-f]{2}[:-])"
                     + "{5}([0-9A-Fa-f]{2})")
        mac_regex_obj = re.compile(mac_regex)

        number_regex = "^\d+$"
        number_regex_obj = re.compile(number_regex)

        status_regex = "^(online|offline)$"
        status_regex_obj = re.compile(status_regex)

        if not re.search(ip_regex_obj, words[0]):
            return False
        if not re.search(mac_regex_obj, words[1]):
            return False
        if not re.search(number_regex_obj, words[2]):
            return False
        if not re.search(status_regex_obj, words[3]):
            return False

        return True


class ArpChangeHandler(FileSystemEventHandler):

    def on_modified(self, event):
        if event.is_directory:
            return

        init_files_if_not_exists()

        current_time = math.floor(time.time())

        # store the MAC addresses in the ARP table in a list
        arp_table_mac_list = []
        with open('/proc/net/arp', 'r') as file:
            for line in file:
                for word in line.split():
                    # courtesy of https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
                    mac_regex = ("^([0-9A-Fa-f]{2}[:-])"
                                 + "{5}([0-9A-Fa-f]{2})")
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

        # keep track of which entries to remove
        # (Python does not like removing dictionary entries while iterating over keys of the dictionary)
        to_be_removed = []

        # determine whether entries in 'MAC_addresses' are to be refreshed or removed
        for mac_addr in acl.keys():
            # If a registered MAC address was found in the ARP table, update its time.
            # If the device was offline before, an update will be sent to the server.
            if acl[mac_addr].mac_addr in arp_table_mac_list:
                acl[mac_addr].last_used = current_time
                if entry.status == "offline":
                    acl[mac_addr].status = "online"
                    manage_capabilities.post_status_update(acl[mac_addr].ip, True)

            # If a registered MAC address was not found in the ARP table and
            # has not been connected for at least TTL seconds, remove it from the list.
            elif acl[mac_addr].last_used + TTL < current_time:
                manage_capabilities.remove_device(acl[mac_addr].ip, False)
                to_be_removed.append(mac_addr)

            # MAC address was not in found in the ARP table, but has not yet expired
            # If the device was online before, an update will be sent to the server.
            else:
                if acl[mac_addr].status == "online":
                    acl[mac_addr].status = "offline"
                    manage_capabilities.post_status_update(acl[mac_addr].ip, False)

        # remove the expired entries
        for mac_addr in to_be_removed:
            del acl[mac_addr]

        # overwrite with updated ACL entries
        suffix = '\n' if len(acl) > 0 else ''
        with open("MAC_addresses", 'w') as file:
            file.write('\n'.join(map(lambda x: str(x), acl.values())) + suffix)


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
    # monitoring /proc/net/arp does not work!
    observer.schedule(ArpChangeHandler(),
                      path="/tmp/arp_table", recursive=False)
    observer.start()

    try:
        while True:
            # keep alive
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
