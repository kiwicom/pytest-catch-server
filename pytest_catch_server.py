import socket
import socketserver
import threading
from http.server import BaseHTTPRequestHandler
from types import SimpleNamespace

import pytest


def handler_factory(requests):
    class Handler(BaseHTTPRequestHandler):
        def process_request(self):
            length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(length)
            requests.append({"path": self.path, "method": self.command, "data": data})

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")

        def do_GET(self):
            self.process_request()

        def do_PUT(self):
            self.process_request()

        def do_POST(self):
            self.process_request()

        def do_PATCH(self):
            self.process_request()

        def do_DELETE(self):
            self.process_request()

    return Handler


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


@pytest.fixture(scope="session")
def catch_server_port():
    """Return free port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def background_catch_server(catch_server_port):
    """Run catch server in a thread for whole session.

    Return `SimpleNamespace(host, port, requests)` where `requests` are list of
    catched requests.
    """
    requests = []
    server = ThreadedTCPServer(("", catch_server_port), handler_factory(requests))
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()

    host, port = server.server_address
    yield SimpleNamespace(host=host, port=port, requests=requests)

    server.shutdown()
    server.server_close()


@pytest.fixture
def catch_server(background_catch_server):
    """Return catch server and flushes catched requests between each test.

    Return `SimpleNamespace(host, port, requests)` where `requests` are list of
    catched requests.
    """
    # flush requests before use
    background_catch_server.requests.clear()
    yield background_catch_server
    # flush requests after use
    background_catch_server.requests.clear()
