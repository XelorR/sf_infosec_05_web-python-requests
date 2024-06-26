#!/usr/bin/env python3

import os
import json
import requests
import subprocess


def do_ping_sweep(ip: str, num_of_host: int, verbose=True):
    os_family = os.name.lower()
    os_related_switches = {
        "posix": "c",
        "linux": "c",
        "darwin": "c",
        "nt": "n",  # Windows uses 'nt' instead of 'windows' for os.name
    }
    ip_parts = ip.split(".")
    network_ip = ip_parts[0] + "." + ip_parts[1] + "." + ip_parts[2] + "."
    scanned_ip = network_ip + str(int(ip_parts[3]) + num_of_host)

    # Using subprocess to run the ping command
    response = subprocess.run(
        ["ping", "-" + os_related_switches[os_family], "1", scanned_ip],
        stdout=subprocess.PIPE,
        text=True,
    )

    res = response.stdout.split("\n")
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
    """
    Sends an HTTP request to the specified target using a given method.

    Parameters:
        - target (str): The URL of the server or resource.
        - method (str): The HTTP method ('GET' or 'POST').
        - headers (list[str]): Optional; List of header strings in "header_name:header_value" format.
                               Defaults to None, implying no custom headers are set.
        - payload (any): Optional; Payload data for POST requests. Can be any type supported by the `requests` library.
                          Defaults to None, indicating a GET request without body content.
        - verbose (bool): Whether to print detailed results or not.
        - save_results (bool): Whether to save the response status code, headers, and content to files.

    Returns:
        A tuple of optional printed messages or saved file contents.
    """
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
