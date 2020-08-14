from http_server import HandleRequests
import socketserver
from driver import DriversDB
from functools import partial


class Aggregator:
    def __init__(self, name, _id, port):
        self.name = name
        self.id = _id
        self.port = port
        self.drivers = DriversDB()  # emulates connection to drivers data base

    def add_driver(self, full_name, license_id):
        self.drivers.add_driver(full_name, license_id)

    def run(self):
        # using partial to forward our aggregator
        # passing self by ref using a list
        handler = partial(HandleRequests, [self, ])
        try:
            with socketserver.TCPServer(("", self.port), handler) as httpd:
                print(f"{self.name} (id {self.id}) serving at port {self.port}")
                httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
