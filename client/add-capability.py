#!/usr/bin/python3

import os
import argparse
import manage_capabilities

if __name__ == "__main__":
    path, _ = os.path.split(os.path.realpath(__file__))
    os.chdir(path)

    parser = argparse.ArgumentParser(
        description="Utility to expose a capability to the federated lab from this bundle box.")

    parser.add_argument("-i", "--ip", metavar="ip_addr", type=str, required=True,
                        help="The IP address of the device for which you want to add a capability.")

    parser.add_argument("-p", "--port", metavar="device_port", type=str, required=True,
                        help="The port of the device for which you want to add a capability.")

    parser.add_argument("-n", "--name", metavar="capability_name", type=str, required=True,
                        help="The name of the capability as it will show up in the capability directory.")

    parser.add_argument("-d", "--description", metavar="capability_desc", type=str, required=True,
                        help="The description of the capability as it will show up in the capability directory.")

    args = parser.parse_args()

    manage_capabilities.add_capability(
        args.ip, args.port, args.name, args.description)
    manage_capabilities.pretty_print_directory()  # todo: remove
