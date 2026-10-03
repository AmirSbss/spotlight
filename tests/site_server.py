#!/usr/bin/env python3
"""Fixture server for test_site.sh: serves tests/fixtures/site on a free port (printed first), except /hang/...,
which never answers, like a stalled font CDN."""
import functools
import http.server
import threading
from pathlib import Path


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/hang/"):
            threading.Event().wait()
        return super().do_GET()

    def log_message(self, *args):
        pass


root = Path(__file__).resolve().parent / "fixtures/site"
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Handler, directory=str(root)))
srv.daemon_threads = True
print(srv.server_address[1], flush=True)
srv.serve_forever()
