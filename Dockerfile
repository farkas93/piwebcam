FROM balenalib/raspberrypi0-2w-64-debian-python

WORKDIR /root

RUN apt update
RUN apt upgrade

RUN apt install -y python3-libcamera python3-kms++
RUN apt install -y python3-picamera2 --no-install-recommends
# RUN sudo apt install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 python3-dev -y
RUN apt install python3-opencv

COPY requirements.txt /root/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY camera_streaming /root/camera_streaming
COPY main.py /root/main.py


CMD [ "python", "main.py" ]
