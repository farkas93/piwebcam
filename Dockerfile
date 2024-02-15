FROM balenalib/raspberrypi3-64-python

WORKDIR /root

RUN install_packages python3-picamera2
RUN install_packages python3-opencv

# Run the app
COPY camera_streaming /root/camera_streaming
COPY main.py /root/main.py

CMD [ "python", "main.py" ]