import time
import io
import cv2
import numpy as np
from threading import Condition
from .resolutions import *
from .face_recognition import ModelType, FaceDetector

import logging

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput


class CameraOutput(io.BufferedIOBase):
    def __init__(self, model_type = None, edge_detection=False):
        self.frame = None
        self.condition = Condition()
        self.edge_detection = edge_detection
        self.face_detector = None
        if model_type != None:
            self.face_detector = FaceDetector(model_type)

    def write(self, buf):
        if self.face_detector != None:
            self.face_detector.detect(buf)
        if self.edge_detection:
            buf = self.canny_edge_detector(buf)
        with self.condition:
            self.frame = buf
            self.condition.notify_all()
    
    
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
    def __init__(self, framerate: float, resolution: tuple, model_type=ModelType.MOBILENET, edge_detection=False):
        self.framerate = framerate

        if model_type == ModelType.RESNET or model_type == ModelType.MOBILENET:
            # Override users settings to make it work with resnet
            self.res = RES_FACE
        else:
            self.res = resolution

        self.picam2 = Picamera2()
        self.configure_camera()
        self.output = CameraOutput(model_type, edge_detection)
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
