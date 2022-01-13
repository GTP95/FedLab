#!/usr/bin/python3

import random
import argparse
import re


def convert_string_to_int_repr(ip_string):
    starting_list = list(map(int, ip_string.split('.')))

    byte_1 = starting_list[0] * 256 * 256 * 256
    byte_2 = starting_list[1] * 256 * 256
    byte_3 = starting_list[2] * 256
    byte_4 = starting_list[3]

    return byte_1 + byte_2 + byte_3 + byte_4


def convert_int_to_string_repr(ip_int):
    result = "{}.{}.{}.{}".format(
        (ip_int >> 24) & 0xff,  # first byte
        (ip_int >> 16) & 0xff,  # second byte
        (ip_int >> 8) & 0xff,   # third byte
        ip_int & 0xff           # fourth byte
    )

    return result


def get_random_ip(range_start, range_end):
    range_start = convert_string_to_int_repr(range_start)
    range_end = convert_string_to_int_repr(range_end)

    random_ip_int = random.randint(range_start, range_end)
    return convert_int_to_string_repr(random_ip_int)


def get_random_unused_ip(range_start, range_end):
    with open('MAC_addresses', 'r') as f:
        existing_ip_assignments = re.findall(
            r'[0-9]+(?:\.[0-9]+){3}', f.read())

    # try generating random IP's in range until we get one that is not in use
    while True:
        random_ip = get_random_ip(range_start, range_end)
        if random_ip not in existing_ip_assignments:
            return random_ip


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Get a random unused IP in a range')
    parser.add_argument('range_start', metavar='start', type=str,
                        help='the first IP address of the range')
    parser.add_argument('range_end', metavar='end', type=str,
                        help='the final IP address of the range')

    args = parser.parse_args()

    print(get_random_unused_ip(args.range_start, args.range_end))
