import time
import cv2
import threading
import logging

from picamera2 import Picamera2

class CameraStream:
    def __init__(self, framerate: float, resolution: tuple):
        self.freq = 1/framerate
        self.res = resolution
        self.picam2 = Picamera2()
        self.output = None
        self.lock = threading.Lock()
        self.configure_camera()
        self.picam2.start()
        logging.info("INIT CAM")


    def configure_camera(self):
        # Configure the camera here, e.g., resolution
        config = self.picam2.create_still_configuration()
        config['main']['size'] = self.res
        self.picam2.configure(config)
        logging.info("CONFIG CAM")

    def capture_frames(self):
        while True:
            with self.lock:
            # Capture an image to a numpy array, then encode as JPEG
                logging.debug("CAPTURE CAM")
                img = self.picam2.capture_array()
                logging.debug(f"Got image: {img}")
                is_success, buffer = cv2.imencode(".jpg", img)
                if is_success:
                    self.output = buffer.tobytes()
            time.sleep(self.freq)  # Adjust based on your framerate needs