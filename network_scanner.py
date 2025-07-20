#!/usr/bin/env python3

import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target_ip_range",
                        help="Target IP address or IP range (e.g., 192.168.1.1/24)",
                        required=True)
    args = parser.parse_args()
    return args.target_ip_range

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered = scapy.srp(arp_request_broadcast, timeout=1,verbose=False)[0]

    clients_list=[]
    for address in answered:
        client_dict={"IP":address[1].psrc,"MAC" : address[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_results(clients_list):
    print("  IP\t\t\tMAC\n------------------------------------")
    for client in clients_list:
        print(client["IP"]+'\t' + client["MAC"])



scan_result=scan(get_arguments())
if scan_result:
    print_results(scan_result)
else:
    print("No results")