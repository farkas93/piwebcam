FROM balenalib/raspberry-pi-debian-python

WORKDIR /root

RUN apt update
RUN apt upgrade

RUN apt install -y python3-picamera2 --no-install-recommends
RUN apt install python3-opencv

COPY requirements.txt /root/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY camera_streaming /root/camera_streaming
COPY main.py /root/main.py


CMD [ "python", "main.py" ]
