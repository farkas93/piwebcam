FROM python:3.11.8-bullseye

RUN apt update && apt install -y --no-install-recommends gnupg

# Add RPI sources to apt
RUN echo "deb http://archive.raspberrypi.org/debian/ bullseye main" > /etc/apt/sources.list.d/raspi.list \
  && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 82B129927FA3303E

RUN apt update && apt -y upgrade

# Install dependencies
RUN apt update && apt install -y --no-install-recommends \
         python3-pip \
         python3-picamera2 \
     && apt-get clean \
     && apt-get autoremove \
     && rm -rf /var/cache/apt/archives/* \
     && rm -rf /var/lib/apt/lists/*

WORKDIR /root

COPY requirements.txt /root/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
COPY camera_streaming /root/camera_streaming
COPY main.py /root/main.py

CMD [ "python", "main.py" ]