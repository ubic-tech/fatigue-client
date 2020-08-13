from http_server import HandleRequests
import socketserver


class Aggregator:
    def __init__(self, name, _id, port):
        self.name = name
        self.id = _id
        self.port = port

    def run(self):
        handler = HandleRequests
        try:
            with socketserver.TCPServer(("", self.port), handler) as httpd:
                print(f"{self.name} (id {self.id}) serving at port {self.port}")
                httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
