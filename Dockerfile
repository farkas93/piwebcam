FROM balenalib/raspberrypi0-2w-64-debian-python

WORKDIR /root

RUN apt-get update
RUN apt-get upgrade

COPY requirements.txt /root/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY camera_streaming /root/camera_streaming
COPY main.py /root/main.py


CMD [ "python", "main.py" ]
