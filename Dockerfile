FROM balenalib/raspberry-pi-debian-python

WORKDIR /root

COPY camera_streaming /root/camera_streaming
COPY main.py /root/main.py


CMD [ "python", "main.py" ]
