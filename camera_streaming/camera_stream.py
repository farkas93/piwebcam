import time
import cv2
import numpy as np
import threading
from threading import Condition

import logging

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput


class CameraOutput(io.BufferedIOBase):
    def __init__(self, edge_detection=False):
        self.frame = None
        self.condition = Condition()
        self.edge_detection = edge_detection

    def write(self, buf):
        if self.edge_detection:
            # Convert the image buffer to a numpy array
            img_array = np.frombuffer(buf, dtype=np.uint8)
            # Decode the image array into an image
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            # Apply edge detection
            edges = cv2.Canny(img, 100, 200)
            # Encode the result back to JPEG
            _, buf = cv2.imencode('.jpg', edges)
            buf = buf.tobytes()
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class CameraStream:
    def __init__(self, framerate: float, resolution: tuple, edge_detection=False):
        self.freq = 1/framerate
        self.res = resolution
        self.picam2 = Picamera2()
        self.configure_camera()
        self.output = CameraOutput(edge_detection)
        self.picam2.start_recording(JpegEncoder(), FileOutput(self.output))
        logging.info("STARTING CAM")


    def configure_camera(self):
        # Configure the camera here, e.g., resolution
        #config = self.picam2.create_still_configuration()
        config = self.picam2.create_video_configuration()
        config['main']['size'] = self.res
        self.picam2.configure(config)
        logging.info("CONFIG CAM")
