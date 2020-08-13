import http.server
from path_handlers import *
PATH_MAP = {
    "/v1/health": v1_health,
    "/v1/drivers/fatigue": v1_drivers_fatigue,
    "/v1/drivers/online/hourly": v1_drivers_online_hourly,
    "/v1/drivers/online/quarter_hourly": v1_drivers_online_quarter_hourly,
    "/v1/drivers/on_order": v1_drivers_on_order,
}


class HandleRequests(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _get_response(self) -> str:
        try:
            handler = PATH_MAP[self.path]
        except KeyError:
            return ""
        content_len = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_len).decode()
        return handler(self.headers, body)

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._get_response().encode())

    def do_POST(self):
        self._set_headers()
        self.wfile.write(self._get_response().encode())

    def do_PUT(self):
        self.do_POST()
