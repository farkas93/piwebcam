import time
import logging

from http.server import BaseHTTPRequestHandler

PAGE = """\
<html>
<head>
<title>Raspberry Pi - Surveillance Camera</title>
</head>
<body>
<center><h1>Raspberry Pi - Surveillance Camera</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
</body>
</html>
"""

class TestStreamingHandler(BaseHTTPRequestHandler):
        
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(PAGE.encode('utf-8'))
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                with open("test.jpg", "rb") as image:
                    frame = image.read()
                while True:
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
                    time.sleep(0.1)  # Adjust based on the framerate
            except Exception as e:
                logging.info("Stream stopped")
                logging.error(e)

class StreamingHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        camera_stream = self.server.camera_stream 
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(PAGE.encode('utf-8'))
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    logging.debug("before capture camera")
                    with camera_stream.lock:
                        frame = camera_stream.output
                        logging.debug(f"capturing frame {frame}")
                        if frame is not None:
                            self.wfile.write(b"--FRAME\r\n")
                            self.wfile.write(b"Content-Type: image/jpeg\r\n\r\n")
                            self.wfile.write(frame)
                            self.wfile.write(b"\r\n")
                    time.sleep(camera_stream.freq)  # Adjust based on the framerate
            except Exception as e:
                logging.info("Stream stopped")
                logging.error(e)