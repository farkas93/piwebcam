FROM debian:bookworm AS bookworm-picamera2
# Build the OS.

RUN apt update && apt install -y --no-install-recommends gnupg

RUN echo "deb http://archive.raspberrypi.org/debian/ bookworm main" > /etc/apt/sources.list.d/raspi.list \
  && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 82B129927FA3303E

RUN apt update && apt -y upgrade

RUN apt install -y --no-install-recommends \
         python3-pip \
         python3-picamera2

RUN apt install -y --no-install-recommends python3-opencv

# Cleanup container
RUN  apt-get clean \
     && apt-get autoremove 
    # Include again once development phase on this repo is finished.
    #  && rm -rf /var/cache/apt/archives/* \
    #  && rm -rf /var/lib/apt/lists/*

# Enable installation of pip packages within python 3.11
RUN rm /usr/lib/python3.11/EXTERNALLY-MANAGED

FROM bookworm-picamera2
# Copy the code, install python packages and start the app

# WORKDIR /root

# # Install dlib
# RUN git clone https://github.com/davisking/dlib

# WORKDIR /root/dlib
# RUN py -m pip install cmake
# RUN py setup.py install

WORKDIR /root

COPY requirements.txt /root/requirements.txt
RUN pip install -r requirements.txt

# Copy detector models to the container
COPY facial_recognition/res10_300x300_ssd_iter_140000.caffemodel /root/resnet/model.caffemodel
COPY facial_recognition/deploy.prototxt.txt /root/resnet/deploy.prototxt
COPY facial_recognition/cascades /root/cascades
COPY facial_recognition/mobilenet_ssd/MobileNetSSD_deploy.caffemodel /root/mobilenet_ssd/model.caffemodel
COPY facial_recognition/mobilenet_ssd/MobileNetSSD_deploy.prototxt /root/mobilenet_ssd/deploy.prototxt

COPY camera_streaming /root/camera_streaming
COPY main.py /root/main.py

CMD [ "python3", "main.py" ]
