#!/usr/bin/env python

import subprocess
import optparse
import re


def get_options():
    parser = optparse.OptionParser()
    parser.add_option(
        "-i", "--interface", dest="interface", help="Target network interface."
    )
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address.")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface. Use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify an new MAC address. Use --help for more info.")

    return options


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


options = get_options()

current_mac = str(get_current_mac(options.interface))
print("Current MAC: " + current_mac)

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac != options.new_mac:
    print("[-] Changing MAC address failed")
else:
    print("[+] MAC address successfully changed to " + current_mac)
