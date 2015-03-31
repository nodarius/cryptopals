#!/usr/bin/python3

import http.server
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import parse_qs

HOST_NAME = 'example.com'
PORT_NUMBER = 80



class Handler(BaseHTTPRequestHandler):
    def do_GET(s):
        print(s.path)
        qs = parse_qs(urlparse(s.path).query)
        filename = qs['file'][0]
        mac = qs['mac'][0]
        print(filename)
        print(mac)

        s.send_response(200)
        s.end_headers()


def run():
    server_address = ('', 8080)
    httpd = http.server.HTTPServer(server_address, Handler)
    httpd.serve_forever()

if __name__ == "__main__":

    run()
