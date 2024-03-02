import time
import io
import cv2
import numpy as np
from threading import Condition, Lock
from .resolutions import *
from .face_recognition import ModelType, FaceDetector

import logging

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput


class CameraOutput(io.BufferedIOBase):
    def __init__(self, img_size, model_type = None, edge_detection=False):
        self.mutex = Lock()
        self.write_pending = False  # Flag to indicate a pending write operation
        self.read_pending = False
        self.edge_detection = edge_detection
        self.face_detector = None
        self.current_frame = self.init_current_frame(img_size=img_size)
        self.latest_frame = None
        if model_type != None:
            self.face_detector = FaceDetector(model_type)

    def init_current_frame(self, img_size):
        """
        Inititalize the current frame to be black.
        """
        black_img = np.zeros(img_size, dtype=np.uint8)
        _, buf = cv2.imencode('.jpg', black_img)
        return buf.tobytes()


    def read(self):
        # Implement a read method to fetch the latest frame
        mutex_available = self.mutex.acquire(blocking=False)
        try:
            if mutex_available and not self.write_pending:
                if self.latest_frame is not None:
                    if self.face_detector != None:
                        self.latest_frame =  self.face_detector.detect(self.latest_frame)
                    if self.edge_detection:
                        self.latest_frame = self.canny_edge_detector(self.latest_frame)
                    self.current_frame = self.latest_frame
                    self.latest_frame = None  # Reset the latest frame to ensure old frames are discarded
                self.read_pending = False
        finally:
            if mutex_available:
                self.mutex.release()
        return self.current_frame        

    def write(self, buf):
        if not self.read_pending:
            self.write_pending = True  # Indicate a write operation is pending
        
        mutex_available = self.mutex.acquire(blocking=False)
        try:
            self.latest_frame = buf
            self.read_pending = True
            self.write_pending = False
        finally:
            if mutex_available:
                self.mutex.release()
        self.flush() # To increase the likelihood that the next frame processed is a recent one. 
    
    
    def canny_edge_detector(self,buf):
        # Convert the image buffer to a numpy array
        img_array = np.frombuffer(buf, dtype=np.uint8)
        # Decode the image array into an image
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        # Apply edge detection
        edges = cv2.Canny(img, 100, 200)
        # Encode the result back to JPEG
        _, buf = cv2.imencode('.jpg', edges)
        return buf.tobytes()


class CameraStream:
    def __init__(self, framerate: float, resolution: tuple, model_type=ModelType.RESNET, edge_detection=False):
        self.framerate = framerate

        if model_type == ModelType.RESNET or model_type == ModelType.MOBILENET:
            # Override users settings to make it work with resnet
            self.res = RES_FACE
        else:
            self.res = resolution

        self.picam2 = Picamera2()
        self.configure_camera()
        self.output = CameraOutput(resolution + (3,), model_type, edge_detection)
        self.picam2.start_recording(JpegEncoder(), FileOutput(self.output))
        logging.info("STARTING CAM")


    def configure_camera(self):
        # Configure the camera here, e.g., resolution
        config = self.picam2.create_video_configuration()
        logging.info(f"CONFIG looks like:\n{config}")
        config['controls']['FrameRate'] = self.framerate        
        config['main']['size'] = self.res
        self.picam2.configure(config)
        logging.info(f"CAMERA CONFIGURED\nRES: {self.res}\nFRAMERATE:{self.framerate}")
