FROM resin/raspberry-pi-python:3

WORKDIR /root

RUN pip install --upgrade pip

COPY requirements.txt /root/requirements.txt
RUN pip install -r requirements.txt

COPY camera_streaming /root/camera_streaming
COPY main.py /root/main.py


CMD [ "python", "main.py" ]
