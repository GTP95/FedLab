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
        if event.is_directory:
            return

        mac_list = []
        current_time = math.floor(time.time())

        with open('home/maxm/Documents/seminar/dummy.txt', 'r') as file:
            for line in file:
                for word in line.split():
                    # courtesy of https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
                    mac_regex = ("^([0-9A-Fa-f]{2}[:-])" +
                            "{5}([0-9A-Fa-f]{2})")            
                    mac_regex_obj = re.compile(mac_regex)

                    if re.search(mac_regex_obj, word):
                        mac_list.append(word)


        new_mac_addr_list = []
        with open("home/maxm/Documents/seminar/MAC_addresses.txt", 'r') as file:
            # copy all entries from arp table
            for mac in mac_list:
                # print("copying from mac_list: {}".format(mac))
                new_mac_addr_list.append("{} {}".format(mac, current_time))

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


        with open("home/maxm/Documents/seminar/MAC_addresses.txt", 'w') as file:
            file.write('\n'.join(new_mac_addr_list))


if __name__ == "__main__":
    os.chdir('/')

    observer = Observer()
    observer.schedule(arp_change_handler(), path=sys.argv[1], recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
        else:
            print("got it")
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
