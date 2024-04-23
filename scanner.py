#!/usr/bin/env python3

"""
Пример команды, которая может быть выполнена в CLI:

python3 scanner.py sendhttp -t https://google.com -m GET -hd Accept-Language:ru

  scanner.py — название файла с кодом утилиты;
  sendhttp — название задачи, которую требуется решить
    (в данном случае это отправка HTTP-запросов,
    также есть задание scan, которое осуществляет сканирование сети);
  -t — аргумент, который указывается для задания цели для отправки HTTP-запроса;
  -m — аргумент, который указывается для задания типа запроса (POST или GET);
  -hd — аргумент, который указывается для задания заголовков.
"""

import os
import json
import argparse
import requests
from platform import system

ip = "10.0.0.1"
num_of_host = 254


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


def main():
    parser = argparse.ArgumentParser(description="Network scanner")
    parser.add_argument(
        "task", choices=["scan", "sendhttp", "server"], help="Network scan or send HTTP request"
    )
    parser.add_argument("-i", "--ip", type=str, help="IP address")
    parser.add_argument("-n", "--num_of_hosts", type=int, help="Number of hosts")

    parser.add_argument(
        "-t", "--target", type=str, help="Target for sending HTTP request"
    )
    parser.add_argument(
        "-m",
        "--method",
        type=str,
        choices=["GET", "POST"],
        help="Method of HTTP request",
    )
    parser.add_argument(
        "-hd", "--headers", type=str, nargs="+", help="HTTP headers (name:value)"
    )

    args = parser.parse_args()
    if args.task == "scan":
        for host_num in range(args.num_of_hosts):
            ip, resp = do_ping_sweep(args.ip, host_num)
            result = [
                row
                for row in resp
                if "packets transmitted" in row
                or "отправлено =" in row
                or "Sent =" in row
            ][0]
            print(
                f"[#] Result of scanning: {ip} [#]\n{result}",
                end="\n\n",
            )
    elif args.task == "sendhttp":
        response = sent_http_request(args.target, args.method, headers=args.headers)
        header = json.dumps(dict(response.headers), indent=4, sort_keys=True)
        print(
            f"[#] Response status code: {response.status_code}\n"
            f"[#] Response headers: {header}\n"
            f"[#] Response content:\n {response.text}"
        )
        with open("status.txt", "w") as f:
            f.write(str(response.status_code))
        with open("headers.json", "w") as f:
            f.write(header)
        with open("response.html", "w") as f:
            f.write(response.text)
    elif args.task == "server":
        pass


if __name__ == "__main__":
    main()
