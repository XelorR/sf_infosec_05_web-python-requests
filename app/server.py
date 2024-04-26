from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import socket
from app.lib import *

"""
sendhttp example:
Пользователь может отправить POST-запрос на 192.168.1.10:3000/sendhttp со следующим телом запроса:

{"Header": "Content-type", "Header-value": "text", "Target":"www.google.com", "Method": "GET"}

scan example:
Пользователь может отправить GET-запрос на 192.168.1.10:3000/scan со следующим телом запроса:

{"target":"192.168.1.0", "count": "20"}
"""


# API Handler
class MyHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/sendhttp":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            headers = {data["Header"]: data["Header-value"]}
            response = requests.get(data["Target"], headers=headers)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(response.text.encode("utf-8"))

    def do_GET(self):
        if self.path == "/scan":
            content_length = int(self.headers["Content-Length"])
            get_data = self.rfile.read(content_length)
            data = json.loads(get_data)

            result = []
            for i in range(1, int(data["count"]) + 1):
                ip = data["target"] + "." + str(i)
                try:
                    socket.gethostbyaddr(ip)
                    result.append(ip + " is active")
                except socket.herror:
                    result.append(ip + " is inactive")

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))


def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ("127.0.0.1", 3000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
