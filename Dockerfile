FROM balenalib/raspberrypi0-2w-64-alpine-python:14.21-3.12

WORKDIR /root

COPY camera_streaming /root/camera_streaming
COPY main.py /root/main.py


CMD [ "python", "main.py" ]
