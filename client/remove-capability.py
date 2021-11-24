#!/usr/bin/python3

import os
import argparse
import manage_capabilities

if __name__ == "__main__":
    path, _ = os.path.split(os.path.realpath(__file__))
    os.chdir(path)

    parser = argparse.ArgumentParser(
        description="Utility to manage the capabilities exposed by the bundle box.")

    parser.add_argument("-i", "--id", metavar="capability_id", type=str, required=True,
                        help="The ID of the to-be-removed capability.")

    args = parser.parse_args()

    manage_capabilities.remove_capability(args.id)
    manage_capabilities.pretty_print_directory()  # todo: remove
