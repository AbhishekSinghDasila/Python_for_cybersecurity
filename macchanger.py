#!/usr/bin/env python3

import subprocess
import argparse # Import the argparse module instead of optparse
import re

def get_arguments_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface",
                        help="Interface to change its MAC address", required=True)
    parser.add_argument("-m", "--mac", dest="new_mac",
                        help="New MAC address", required=True)
    args = parser.parse_args()
    return args

def mac_changer(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    print("[+] Interface brought up.")

def get_current_mac_address(interface):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
        if mac_address_search_result:
            return mac_address_search_result.group(0)
        else:
            print(f"[-] Could not find MAC address for interface {interface}.")
            return None # Return None explicitly if not found
    except subprocess.CalledProcessError as e:
        print(f"[-] Error running ifconfig for {interface}: {e}")
        print("    Please ensure the interface exists and you have sufficient permissions.")
        return None
    except FileNotFoundError:
        print("[-] 'ifconfig' command not found. Please install net-tools or use 'ip' command.")
        return None

options = get_arguments_argparse()

current_mac_address = get_current_mac_address(options.interface)
if current_mac_address:
    print(f"Current MAC address for {options.interface} is {current_mac_address}")
else:
    print(f"[-] Failed to retrieve current MAC address for {options.interface}. Exiting.")
    exit()

if current_mac_address == options.new_mac:
    print(f"[!] MAC address for {options.interface} is already {options.new_mac}. No change needed.")
else:
    mac_changer(options.interface, options.new_mac)

    current_mac_address_after_change = get_current_mac_address(options.interface)
    if current_mac_address_after_change == options.new_mac:
        print("[+] MAC address changed successfully!")
    else:
        print("[-] MAC address change failed.")
        print(f"    Current MAC: {current_mac_address_after_change}, Desired MAC: {options.new_mac}")