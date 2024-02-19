FROM balenalib/raspberrypi3-64-python AS bullseye-picamera2
# Build the OS.

RUN install_packages python3-picamera2

FROM bullseye-picamera2
# Copy the code and start the app

WORKDIR /root

COPY requirements.txt /root/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY camera_streaming /root/camera_streaming
COPY main.py /root/main.py

CMD [ "python3", "main.py" ]
