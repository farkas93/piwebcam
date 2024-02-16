FROM balenalib/raspberrypi3-64:latest

WORKDIR /root

# Install correct python version. In my case 3.11. Has to be the same as on your host
RUN install_packages build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
RUN wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz
RUN tar -xvf Python-3.11.3.tgz

WORKDIR /root/Python-3.11.3
RUN ./configure --enable-optimizations
#adjust the number to be the number of processors on your pi
RUN make -j 4

# Install the python packages from the repo
RUN install_packages python3-picamera2
RUN install_packages python3-opencv
RUN pip install --upgrade pip

WORKDIR /root
COPY requirements.txt /root/requirements.txt
RUN pip install -r requirements.txt

# Run the app
COPY camera_streaming /root/camera_streaming
COPY main.py /root/main.py

CMD [ "python", "main.py" ]