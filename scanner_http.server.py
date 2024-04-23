from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import socket


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
    server_address = ("192.168.1.10", 3000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
