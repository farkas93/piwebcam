FROM balenalib/raspberrypi0-2w-64-debian-python

WORKDIR /root

RUN apt-get update
RUN apt-get upgrade

RUN apt-get install build-essential libcap-dev libgl1-mesa-glx ffmpeg libsm6 libxext6 -y
RUN apt-get instal python3-libcamera

COPY requirements.txt /root/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY camera_streaming /root/camera_streaming
COPY main.py /root/main.py


CMD [ "python", "main.py" ]
