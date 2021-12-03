#!/usr/bin/python3

import os
import argparse
import manage_capabilities

if __name__ == "__main__":
    path, _ = os.path.split(os.path.realpath(__file__))
    os.chdir(path)

    parser = argparse.ArgumentParser(
        description="Utility to manage the devices exposed by the bundle box.")

    parser.add_argument("-m", "--mac", metavar="mac_addr", type=str, required=True,
                        help="The MAC address of the device you want to connect/expose.")

    parser.add_argument('-e', "--expose", dest="expose_device", action='store_true',
                        help="Use -e to expose the device to the entire network. Without -e only add the device to the ACL.")

    parser.add_argument("-n", "--name", metavar="device_name", type=str,
                        help="[Only necessary with the -e flag] The name of the device you want to expose as it will show up in the device directory.")

    parser.add_argument("-d", "--desc", metavar="device_desc", type=str,
                        help="[Only necessary with the -e flag] The description of the device you want to expose as it will show up in the device directory. Also include the name of the device's manual, if any, such that others are easily able to retrieve it.")

    args = parser.parse_args()

    manage_capabilities.check_args(
        args.mac, args.name, args.desc, args.expose_device)
    manage_capabilities.pretty_print_directory()  # todo: remove
