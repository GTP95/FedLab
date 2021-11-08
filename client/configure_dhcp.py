#!/usr/bin/python3

import re
import subprocess


def write_existing_entries():
    with open('MAC_addresses', 'r') as f:
        lines = f.readlines()

    for line in lines:
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)[0]

        # finding mac with re.findall acted weirdly
        mac_regex = ("([0-9A-Fa-f]{2}[:-])"
                     + "{5}([0-9A-Fa-f]{2})|"
                     + "([0-9a-fA-F]{4}\\."
                     + "[0-9a-fA-F]{4}\\."
                     + "[0-9a-fA-F]{4})")

        # Compile the ReGex
        p = re.compile(mac_regex)

        mac = re.search(p, line).group()

        write_device_entry(mac, ip)


def write_device_entry(mac, ip):
    with open('/etc/dhcp/dhcpd.conf', 'a') as f:
        f.writelines(
            "\nhost device-{} {{\n  hardware ethernet {};\n  fixed-address {};\n}}\n".format(
                subprocess.check_output(
                    ['uuidgen']).decode('utf-8').strip(), mac, ip
            ))


if __name__ == "__main__":
    write_existing_entries()
