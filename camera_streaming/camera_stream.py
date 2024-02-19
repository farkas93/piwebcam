import time
import io
import os
import cv2
import numpy as np
from threading import Condition
from .resolutions import *

import logging

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput


class CameraOutput(io.BufferedIOBase):
    def __init__(self, edge_detection=False, face_detection=False):
        self.frame = None
        self.condition = Condition()
        self.edge_detection = edge_detection
        self.face_detection = face_detection
        if face_detection:
            cwd = os.getcwd()
            modelFile = cwd + "/resnet.caffemodel"
            configFile = cwd + "/deploy.prototxt"
            self.net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
            logging.info(f"initialized model {modelFile}")


    def write(self, buf):
        if self.face_detection:
            buf = self.resnet_face_detection(buf)
        if self.edge_detection:
            buf = self.canny_edge_detector(buf)
        with self.condition:
            self.frame = buf
            self.condition.notify_all()
    
    def resnet_face_detection(self,buf):

        # Convert the image buffer to a numpy array
        img_array = np.frombuffer(buf, dtype=np.uint8)
        # Decode the image array into an image
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
         # Prepare the frame to be fed to the network
        blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), (104.0, 177.0, 123.0))

        # Set the input to the network
        self.net.setInput(blob)

        # Forward pass to get the network's output
        detections = self.net.forward()

        # Draw detections on the frame
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:  # Confidence threshold
                box = detections[0, 0, i, 3:7] * np.array([300, 300, 300, 300])
                (startX, startY, endX, endY) = box.astype("int")

                # Draw the bounding box of the face along with the associated probability
                text = "{:.2f}%".format(confidence * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)
                cv2.putText(img, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

        _, buf = cv2.imencode('.jpg', img)
        return buf.tobytes()

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
    def __init__(self, framerate: float, resolution: tuple, edge_detection=False, face_detection=True):
        self.framerate = framerate

        if face_detection:
            # Override users settings to make it work with resnet
            self.res = RES_FACE
        else:
            self.res = resolution

        self.picam2 = Picamera2()
        self.configure_camera()
        self.output = CameraOutput(edge_detection, face_detection)
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
