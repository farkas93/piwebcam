import cv2
import logging
import os
from enum import Enum
import numpy as np


class ModelType(Enum):
    HAARCASCADE = 1
    RESNET = 2
    MOBILENET = 3

class FaceDetector():
    def __init__(self, model_type:ModelType):
        cwd = os.getcwd()
        if model_type == ModelType.RESNET:
            modelFile = cwd + "/resnet/model.caffemodel"
            configFile = cwd + "/resnet/deploy.prototxt"
            self.net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
            self.detect = self._dnn_face_detection
        elif(model_type == ModelType.MOBILENET):
            modelFile = cwd + "/mobilenet_ssd/model.caffemodel"
            configFile = cwd + "/mobilenet_ssd/deploy.prototxt"
            self.net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
            self.detect = self._dnn_face_detection
        else:
            modelFile = cwd + '/cascades/haarcascade_frontalface_default.xml'
            self.cascade = cv2.CascadeClassifier(modelFile)
            self.detect = self._cascade_face_detection

        logging.info(f"INITIALIZED MODEL {model_type}\nModelFile: {modelFile}")

    def _cascade_face_detection(self, buf):

        # Convert the image buffer to a numpy array
        img_array = np.frombuffer(buf, dtype=np.uint8)
        # Decode the image array into an image
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        _, buf = cv2.imencode('.jpg', img)
        return buf.tobytes()

    def _dnn_face_detection(self, buf):

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