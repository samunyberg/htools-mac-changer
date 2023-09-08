#!/usr/bin/env python

import subprocess
import optparse


def get_options():
    parser = optparse.OptionParser()
    parser.add_option(
        "-i", "--interface", dest="interface", help="Target network interface."
    )
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address.")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface. Use ––help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify an new MAC address. Use ––help for more info.")

    return options


def change_mac(interface, new_mac):
    print("Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


options = get_options()
change_mac(options.interface, options.new_mac)
