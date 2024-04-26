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

import argparse
from platform import system
from app.lib import *

ip = "10.0.0.1"
num_of_host = 254


def main():
    # part one, parsing arguments
    parser = argparse.ArgumentParser(description="Network scanner")
    parser.add_argument(
        "task",
        choices=["scan", "sendhttp", "server"],
        help="Network scan or send HTTP request",
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
    
    # ping sweep
    if args.task == "scan":
        for host_num in range(args.num_of_hosts):
            ip, resp = do_ping_sweep(args.ip, host_num)

    # sending http request
    elif args.task == "sendhttp":
        response = sent_http_request(args.target, args.method, headers=args.headers)

    # running server
    elif args.task == "server":
        from app import server

        print("Server is running.\nPress Control-C to stop.\n")
        server.run()


if __name__ == "__main__":
    main()
