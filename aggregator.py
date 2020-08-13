from http_server import HandleRequests
import socketserver


class Aggregator:
    def __init__(self, name, _id, port):
        self.name = name
        self.id = _id
        self.port = port
        self.drivers = {}

    def add_driver(self, driver):
        k, v = driver
        self.drivers[k] = v

    def set_fatigue(self, driver_id, val):
        self.drivers[driver_id] = val

    def set_last_hour(self, driver_id, val):
        self.drivers[driver_id] = val

    def set_last_quarters(self, driver_id, values):
        self.drivers[driver_id] = [val for val in values[:4]]

    def get_fatigue(self, driver_id,):
        return self.drivers[driver_id].fatigue

    def get_last_hour(self, driver_id,):
        return self.drivers[driver_id].last_hour

    def get_last_quarters(self, driver_id,):
        return self.drivers[driver_id].last_quarters

    def run(self):
        handler = HandleRequests
        try:
            with socketserver.TCPServer(("", self.port), handler) as httpd:
                print(f"{self.name} (id {self.id}) serving at port {self.port}")
                httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
