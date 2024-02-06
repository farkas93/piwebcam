import time
import cv2
import threading
import logging

from picamera2 import Picamera2

class CameraStream:
    def __init__(self):
        self.picam2 = Picamera2()
        self.output = None
        self.lock = threading.Lock()
        self.configure_camera()
        logging.info("INIT CAM")

    def configure_camera(self):
        # Configure the camera here, e.g., resolution
        config = self.picam2.create_still_configuration()
        config['main']['size'] = (640, 480)
        self.picam2.configure(config)
        logging.info("CONFIG CAM")

    def capture_frames(self):
        logging.info("CAPTURE CAM")
        while True:
            #with self.lock:
            # Capture an image to a numpy array, then encode as JPEG
            img = self.picam2.capture_array()
            logging.info(f"Got image: {img}")
            is_success, buffer = cv2.imencode(".jpg", img)
            if is_success:
                self.output = buffer.tobytes()
            time.sleep(10)  # Adjust based on your framerate needs