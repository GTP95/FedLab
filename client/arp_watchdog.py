import time
import sys
import os
import logging
import time
import re
from watchdog.observers import Observer
from watchdog.events import *
import math


# 5 days
TTL = 5*24*60*60

class arp_change_handler(FileSystemEventHandler):
    def is_valid_line(self, line):
        words = line.split()
        if len(words) != 2:
            return False

        # courtesy of https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
        mac_regex = ("^([0-9A-Fa-f]{2}[:-])" +
                "{5}([0-9A-Fa-f]{2})")            
        mac_regex_obj = re.compile(mac_regex)

        number_regex = "^\d+$"
        number_regex_obj = re.compile(number_regex)

        if not re.search(mac_regex_obj, words[0]):
            return False
        if not re.search(number_regex_obj, words[1]):
            return False

        return True


    def on_modified(self, event):
        if event.is_directory:
            return

        current_time = math.floor(time.time())

        # store the MAC addresses in the ARP table in a list
        arp_table_mac_list = []
        with open('/tmp/arp_table', 'r') as file:
            for line in file:
                for word in line.split():
                    # courtesy of https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
                    mac_regex = ("^([0-9A-Fa-f]{2}[:-])" +
                            "{5}([0-9A-Fa-f]{2})")            
                    mac_regex_obj = re.compile(mac_regex)

                    if re.search(mac_regex_obj, word):
                        arp_table_mac_list.append(word)

        # determine whether entries in 'MAC_addresses' are to be refreshed or removed
        new_mac_addr_list = []
        with open("MAC_addresses", 'r') as file:
            for line in file:
                if not self.is_valid_line(line):
                    print("A line in MAC_addresses was invalid: " + repr(line))
                    continue
                
                mac_addr = line.split()[0]

                # if a registered MAC address was found in the ARP table, update its time
                if mac_addr in arp_table_mac_list:
                    new_mac_addr_list.append("{} {}".format(mac_addr, current_time))
                # If a registered MAC address was not found in the ARP table and
                # has not been connected for at least TTL seconds, remove it from the list.
                elif int(line.split()[1]) + TTL < current_time:
                    # TODO: run arpRules.sh with delete mac address
                    pass
                # MAC address was not in found in the ARP table, but has not yet expired
                else:
                    new_mac_addr_list.append(line.strip('\n'))

            print(new_mac_addr_list)

            # new_mac_addr_list[:] = map(lambda x: x.strip('\x00'), new_mac_addr_list)

        suffix = '\n' if len(new_mac_addr_list) > 0 else ''
        with open("MAC_addresses", 'w') as file:
            file.write('\n'.join(new_mac_addr_list) + suffix)


def init_files():
    if not os.path.exists("arp_table"):
        open("/tmp/arp_table", 'w').close()

    if not os.path.exists("MAC_addresses"):
        open("MAC_addresses", 'w').close()


if __name__ == "__main__":
    path, _ = os.path.split(os.path.realpath(__file__))
    os.chdir(path)

    init_files()

    observer = Observer()
    observer.schedule(arp_change_handler(), path="/tmp/arp_table", recursive=False) # monitoring /proc/net/arp does not work!
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
