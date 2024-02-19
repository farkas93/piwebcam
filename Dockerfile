FROM debian:bullseye AS bullseye-python

RUN apt update && apt install -y --no-install-recommends gnupg

RUN echo "deb http://archive.raspberrypi.org/debian/ bullseye main" > /etc/apt/sources.list.d/raspi.list \
  && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 82B129927FA3303E

RUN apt update && apt -y upgrade

RUN apt update && apt install -y --no-install-recommends \
         python3-pip \
         python3-picamera2 \
     && apt-get clean \
     && apt-get autoremove \
     && rm -rf /var/cache/apt/archives/* \
     && rm -rf /var/lib/apt/lists/*

FROM bullseye-python

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python files
COPY pi_camera_in_docker /app/pi_camera_in_docker

# Set the entry point
CMD ["python3", "/app/pi_camera_in_docker/main.py"]

# # Install the python packages from the repo
# RUN install_packages python3-pip
# RUN pip install --upgrade pip
# RUN install_packages python3-picamera2
# RUN install_packages python3-opencv

# COPY requirements.txt /root/requirements.txt
# RUN pip install -r requirements.txt

# # Run the app
# COPY camera_streaming /root/camera_streaming
# COPY main.py /root/main.py

# CMD [ "python", "main.py" ]