from http_server import HandleRequests
import socketserver
from driver import DriversDB


class Aggregator:
    def __init__(self, name, _id, port):
        self.name = name
        self.id = _id
        self.port = port
        self.drivers = DriversDB()  # emulates connection to drivers data base

    def add_driver(self, full_name, license_id):
        self.drivers.add_driver(full_name, license_id)

    def set_fatigue(self, driver_id, val):
        self.drivers.set_fatigue(driver_id, val)

    def set_last_hour(self, driver_id, val):
        self.drivers.set_last_hour(driver_id, val)

    def set_last_quarters(self, driver_id, values):
        self.drivers.set_last_quarters(driver_id, values)

    def get_fatigue(self, driver_id):
        return self.drivers.get_fatigue(driver_id)

    def get_last_hour(self, driver_id):
        return self.drivers.get_last_hour(driver_id)

    def get_last_quarters(self, driver_id):
        return self.drivers.get_last_quarters(driver_id)

    def run(self):
        handler = HandleRequests
        try:
            with socketserver.TCPServer(("", self.port), handler) as httpd:
                print(f"{self.name} (id {self.id}) serving at port {self.port}")
                httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
