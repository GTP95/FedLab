#!/usr/bin/python3

import os
import argparse
import manage_capabilities

if __name__ == "__main__":
    path, _ = os.path.split(os.path.realpath(__file__))
    os.chdir(path)

    parser = argparse.ArgumentParser(
        description="Utility to manage the devices exposed by the bundle box.")

    parser.add_argument("-i", "--ip", metavar="ip_addr", type=str, required=True,
                        help="The IP address of the device you want to expose.")

    parser.add_argument("-n", "--name", metavar="capability_name", type=str, required=True,
                        help="The name of the device you want to expose as it will show up in the device directory.")

    args = parser.parse_args()

    manage_capabilities.add_device(
        args.ip, args.name)
    manage_capabilities.pretty_print_directory()  # todo: remove
