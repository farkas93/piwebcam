import logging
import os

from camera_streaming.resolutions import *
from camera_streaming.http_server import ThreadedHTTPServer
from camera_streaming.streaming_handler import StreamingHandler, TestStreamingHandler
from camera_streaming.camera_stream import CameraStream

try:
    log_level = os.environ['LOG_LEVEL'].upper()
except KeyError:
    log_level = 'INFO'

log_level_mapping = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

logging.basicConfig(level=log_level_mapping.get(log_level, logging.WARNING))


def main():
    framerate = 5.0
    resolution = RES_480P
    run(framerate=framerate, resolution=resolution, handler_class=StreamingHandler)

def run(framerate, resolution, handler_class=StreamingHandler):

    # Start the camera stream
    camera_stream = CameraStream(framerate, resolution, edge_detection=False)

    # Start the web service
    server_address = ('', 8000)
    httpd = ThreadedHTTPServer(server_address, handler_class, camera_stream)
    print('Starting server, use <Ctrl-C> to stop')
    httpd.serve_forever()

if __name__ == '__main__':
    main()