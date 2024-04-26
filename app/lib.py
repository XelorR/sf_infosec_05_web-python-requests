#!/usr/bin/env python3

import os
import json
import requests
from platform import system


def do_ping_sweep(ip: str, num_of_host: str, verbose=True):
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
    if verbose:
        print_ping_results(scanned_ip, res)
    return scanned_ip, res


def print_ping_results(ip, res):
    result = [
        row
        for row in res
        if "packets transmitted" in row or "отправлено =" in row or "Sent =" in row
    ][0]
    print(
        f"[#] Result of scanning: {ip} [#]\n{result}",
        end="\n\n",
    )
    return result


def sent_http_request(
    target: str,
    method: str,
    headers=None,
    payload=None,
    verbose=True,
    save_results=False,
):
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
    header = json.dumps(dict(response.headers), indent=4, sort_keys=True)

    # print out the results
    if verbose:
        print(
            f"[#] Response status code: {response.status_code}\n"
            f"[#] Response headers: {header}\n"
            f"[#] Response content:\n {response.text}"
        )

    # saving results into files
    if save_results:
        with open("status.txt", "w") as f:
            f.write(str(response.status_code))
        with open("headers.json", "w") as f:
            f.write(header)
        with open("response.html", "w") as f:
            f.write(response.text)

    # returning all
    return response
