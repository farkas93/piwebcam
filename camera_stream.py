import time
import cv2
import threading

from picamera2 import Picamera2



class CameraStream:
    def __init__(self):
        self.picam2 = Picamera2()
        self.output = None
        self.lock = threading.Lock()
        self.configure_camera()

    def configure_camera(self):
        # Configure the camera here, e.g., resolution
        config = self.picam2.create_still_configuration()
        self.picam2.configure(config)

    def capture_frames(self):
        while True:
            with self.lock:
                # Capture an image to a numpy array, then encode as JPEG
                img = self.picam2.capture_array()
                print(f"Got image: {img}")
                is_success, buffer = cv2.imencode(".jpg", img)
                if is_success:
                    self.output = buffer.tobytes()
            time.sleep(10)  # Adjust based on your framerate needs