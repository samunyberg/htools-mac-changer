#!/usr/bin/env python

import argparse
import subprocess
import re


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--interface",
        required=True,
        dest="interface",
        help="Target network interface.",
    )
    parser.add_argument(
        "-m", "--mac", required=True, dest="new_mac", help="New MAC address."
    )
    return parser.parse_args()


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = str(subprocess.check_output(["ifconfig", interface]))
    mac_address_search_result = re.search(
        r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result
    )
    if not mac_address_search_result:
        print(
            "[-] Unable to read MAC address for provided interface. Exiting the program..."
        )
        exit()

    return mac_address_search_result.group(0)


args = get_args()

current_mac = str(get_current_mac(args.interface))
print("Current MAC: " + current_mac)

change_mac(args.interface, args.new_mac)

current_mac = get_current_mac(args.interface)
if current_mac != args.new_mac:
    print("[-] Changing MAC address failed")
else:
    print("[+] MAC address successfully changed to " + current_mac)
