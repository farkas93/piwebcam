# PI Webcam

This is a small project to let you use your rpi with your rpi camera module as a virtual webcam.

## Picamera 2 for Bookworm 64-bit with Docker

I set up a docker container with the latest debian bookworm for using it with picamera2 and open-cv.

Credits to [hyzhak](https://github.com/hyzhak/pi-camera-in-docker/tree/main) for giving a good template on that matter.
The main difference is that he is basing his container on bullseye.


## Run this project on your PI

Simply clone the repo to your pi. Make sure to have docker together with docker compose installed.
Use the scripts `init_submodules.sh`to initialize the facial recognition submodule (required by the Dockerfile). Just to be sure also execute `pull_submodules.sh`.
Use `docker compose up -d` to start the service.

## Use it as webcam on your machine
So far I only explored this for linux machines. 

### Prerequisites
The bash script is essentially following these steps.

Install `v4l2loopbac`:

```
sudo apt-get update
sudo apt-get install v4l2loopback-dkms
```

Load the `v4l2loopbac` module
After installing, you need to load the module into the kernel:
```
sudo modprobe v4l2loopback
```
This command will create a new virtual video device on your system, typically /dev/videoX, where X is a number (like 0, 1, etc.). You can check the created device with ls /dev/video*.

Then install `ffmpeg`:
```
sudo apt-get install ffmpeg
```

In the end stream your device with:
```
ffmpeg -i http://MY.IP.AD.RESS:8000/stream.mjpg -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/videoX
```

### Using it
Finally if you have everything installed you can follow these steps to use a convenient bash script to spin up your virtual camera client:
1. Create a copy of the `enable_virtual_webcam.sh.template` file and rename it to `enable_virtual_webcam.sh`.
2. Adjust the `STREAM_URL="http://MY.IP.AD.RESS:8000/stream.mjpg"` in the `enable_virtual_webcam.sh` script to match the IP address of the RPI to which your camera is physically connected.
3. And then run the bash script:
```
chmod +x enable_virtual_webcam.sh
./enable_virtual_webcam.sh
```

## Future work

I am planning to implement face tracking and to combine it with a little mobile robotic manipulator. The idea is to have a little robot as webcam which will track and follow your face. Let's see how it will turn out. That is also the reason why i included face detection support via open-cv.