#!/usr/bin/python3

import os
import argparse
import manage_capabilities

if __name__ == "__main__":
    path, _ = os.path.split(os.path.realpath(__file__))
    os.chdir(path)

    manage_capabilities.pretty_print_directory()
