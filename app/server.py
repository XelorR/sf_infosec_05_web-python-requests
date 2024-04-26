#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from app.lib import *

"""
sendhttp example:
Пользователь может отправить POST-запрос на 192.168.1.10:3000/sendhttp со следующим телом запроса:

{"Header": "Content-type", "Header-value": "text", "Target":"www.google.com", "Method": "GET"}

curl -X POST -H "Content-Type: application/json" -d '{"Header": "Content-type", "Header-value": "text", "Target":"www.google.com", "Method": "GET"}' http://localhost:3000/sendhttp

scan example:
Пользователь может отправить GET-запрос на 192.168.1.10:3000/scan со следующим телом запроса:

{"target":"192.168.1.0", "count": "20"}

curl -X GET -H "Content-Type: application/json" -d '{"target":"192.168.1.0", "count": "20"}' http://localhost:3000/scan
curl -X POST -H "Content-Type: application/json" -d '{"target":"10.0.0.1", "count": "3"}' http://localhost:3000/scan
"""


# API Handler
class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/sendhttp":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            target = data["Target"]
            target = target if target.startswith("http") else f"http://{target}"
            method = data["Method"]
            header = data["Header"]
            header_value = data["Header-value"]
            headers = {header: header_value}
            response = sent_http_request(target, method, headers=headers)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            header_extracted = json.dumps(
                dict(response.headers), indent=4, sort_keys=True
            )

            self.wfile.write(bytes((str(response.status_code)), "utf-8"))
            self.wfile.write(bytes(header_extracted, "utf-8"))
            self.wfile.write(bytes((str(response.text)), "utf-8"))

    def do_GET(self):
        if self.path == "/scan":
            content_length = int(self.headers["Content-Length"])
            get_data = self.rfile.read(content_length)
            data = json.loads(get_data)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            target = data["target"]
            count = data["count"]
            for host_num in range(int(count)):
                ip, resp = do_ping_sweep(target, host_num)
                result = [
                    row
                    for row in resp
                    if "packets transmitted" in row
                    or "отправлено =" in row
                    or "Sent =" in row
                ][0]
                self.wfile.write(
                    bytes(f"\n[#] Result of scanning: {ip} [#]\n{result}\n\n", "utf-8")
                )


def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ("127.0.0.1", 3000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
