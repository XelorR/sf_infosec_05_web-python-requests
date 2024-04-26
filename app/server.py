#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import socket
from app.lib import *

"""
sendhttp example:
Пользователь может отправить POST-запрос на 192.168.1.10:3000/sendhttp со следующим телом запроса:

{"Header": "Content-type", "Header-value": "text", "Target":"www.google.com", "Method": "GET"}
curl -X POST -H '{"Header": "Content-type", "Header-value": "text", "Target":"www.google.com", "Method": "GET"}' http://localhost:3000/sendhttp

scan example:
Пользователь может отправить GET-запрос на 192.168.1.10:3000/scan со следующим телом запроса:

{"target":"192.168.1.0", "count": "20"}
curl -X GET -H '{"target":"192.168.1.0", "count": "20"}' http://localhost:3000/sendhttp
"""


# API Handler
class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/sendhttp":
            target = self.headers["Target"]
            method = self.headers["Method"]
            header = self.headers["Header"]
            header_value = self.headers["Header-value"]
            headers = f"{header}:{header_value}"
            response = sent_http_request(target, method, headers=headers)

    def do_GET(self):
        if self.path == "/scan":
            target = self.headers["target"]
            count = self.headers["count"]
            for host_num in range(count):
                ip, resp = do_ping_sweep(target, host_num)


def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ("127.0.0.1", 3000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
