from http.server import HTTPServer
from socketserver import ThreadingMixIn

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    def __init__(self, server_address, handler_class, camera_stream):
        super().__init__(server_address, handler_class)
        self.camera_stream = camera_stream
        self.allow_reuse_address = True
        self.daemon_threads = True
    