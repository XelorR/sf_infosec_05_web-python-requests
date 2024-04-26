#!/usr/bin/env python3

import os
import requests
from platform import system


def do_ping_sweep(ip, num_of_host):
    os_family = system().lower()
    os_related_switches = {
        "linux": "c",
        "darwin": "c",
        "windows": "n",
    }
    ip_parts = ip.split(".")
    network_ip = ip_parts[0] + "." + ip_parts[1] + "." + ip_parts[2] + "."
    scanned_ip = network_ip + str(int(ip_parts[3]) + num_of_host)
    response = os.popen(f"ping -{os_related_switches[os_family]} 1 {scanned_ip}")
    res = response.readlines()
    return scanned_ip, res


def sent_http_request(target: str, method: str, headers=None, payload=None):
    headers_dict = dict()

    if headers:
        for header in headers:
            header_name = header.split(":")[0]
            header_value = header.split(":")[1:]
            headers_dict[header_name] = ":".join(header_value)

    if method.upper() in ["GET", "DELETE"]:
        response = requests.get(target, headers=headers_dict)
    else:
        response = requests.post(target, headers=headers_dict, data=payload)
    return response
