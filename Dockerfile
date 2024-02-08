FROM balenalib/raspberrypi0-2w-64-python

WORKDIR /root

RUN sudo apt update
RUN sudo apt upgrade
RUN sudo apt install -y python3-picamera2 --no-install-recommends

RUN pip install --upgrade pip

COPY requirements.txt /root/requirements.txt
RUN pip install -r requirements.txt

COPY camera_streaming /root/camera_streaming
COPY main.py /root/main.py


CMD [ "python", "main.py" ]
