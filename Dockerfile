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

WORKDIR /root

COPY requirements.txt /root/requirements.txt
RUN pip install -r requirements.txt

COPY camera_streaming /root/camera_streaming
COPY facial_recognition/res10_300x300_ssd_iter_140000.caffemodel /root/camera_streaming/resnet.caffemodel
COPY facial_recognition/deploy.prototxt.txt /root/camera_streaming/deploy.prototxt
COPY main.py /root/main.py

CMD [ "python3", "main.py" ]
