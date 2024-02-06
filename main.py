import threading

from http_server import ThreadedHTTPServer
from streaming_handler import StreamingHandler, TestStreamingHandler
from camera_stream import CameraStream

def run(handler_class=StreamingHandler):
    # Start the camera stream
    camera_stream = CameraStream()
    threading.Thread(target=camera_stream.capture_frames, daemon=True).start()

    # Start the web service
    server_address = ('', 8000)
    httpd = ThreadedHTTPServer(server_address, handler_class, camera_stream)
    print('Starting server, use <Ctrl-C> to stop')
    httpd.serve_forever()

if __name__ == '__main__':
    run(handler_class=StreamingHandler)
