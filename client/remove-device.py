#!/usr/bin/python3

import os
import argparse
import manage_capabilities

if __name__ == "__main__":
    path, _ = os.path.split(os.path.realpath(__file__))
    os.chdir(path)

    parser = argparse.ArgumentParser(
        description="Utility to remove devices exposed by the bundle box.")

    parser.add_argument("-i", "--ip", metavar="device_ip", type=str, required=True,
                        help="The IP address of the to-be-removed device.")

    parser.add_argument('-a', "--acl", dest="remove_acl", action='store_true',
                        help="Use -a flag to remove the device from the ACL, the device will no longer be connected to the Federated Lab in any way.")

    args = parser.parse_args()

    manage_capabilities.remove_device(args.ip, args.remove_acl)
    manage_capabilities.pretty_print_directory()  # todo: remove
