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
    def on_modified(self, event):
        print("The arp table was altered")

        if event.is_directory:
            return

        print("The arp table was altered")

        mac_list = []
        current_time = math.floor(time.time())

        with open('/proc/net/arp', 'r') as file:
            for line in file:
                for word in line.split():
                    # courtesy of https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
                    mac_regex = ("^([0-9A-Fa-f]{2}[:-])" +
                            "{5}([0-9A-Fa-f]{2})")            
                    mac_regex_obj = re.compile(mac_regex)

                    if re.search(mac_regex_obj, word):
                        mac_list.append(word)


        new_mac_addr_list = []

        # copy all entries from arp table
        for mac in mac_list:
            # print("copying from mac_list: {}".format(mac))
            new_mac_addr_list.append("{} {}".format(mac, current_time))

        if not os.path.exists("MAC_addresses"):
            open("MAC_addresses", 'w').close()

        with open("MAC_addresses", 'r') as file:
            # check for validity of remaining entries
            for line in file:
                if len(line.split()) == 0:
                    pass
                
                mac_addr = line.split()[0].strip('\x00')
                if mac_addr in mac_list:
                    # print("skipping because already copied: {}".format(mac_addr))
                    pass
                elif int(line.split()[1]) + TTL < current_time:
                    # TODO: run arpRules.sh with delete mac address
                    pass
                else:
                    new_mac_addr_list.append(line)

            print(repr(new_mac_addr_list[0]))
            new_mac_addr_list[:] = map(lambda x: x.strip('\x00'), new_mac_addr_list)
            print(repr(new_mac_addr_list[0]))


        with open("MAC_addresses", 'w') as file:
            file.write('\n'.join(new_mac_addr_list))


if __name__ == "__main__":
    path, _ = os.path.split(os.path.realpath(__file__))

    os.chdir(path)

    observer = Observer()
    observer.schedule(arp_change_handler(), path="/proc/net/arp", recursive=False) # monitoring /proc/net/arp does not work!
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
