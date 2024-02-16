# Dirty Picamera2 within a Docker container

I have been playing around with making my code run within a docker container on my RPI zero 2W. 
I believe that currently there is no way to make picamera2 run within a docker container in a smooth manner.
Therefore I propose temporarily a dirty fix.

Please make sure that you adjust the Dockerfile to your install the same python version as you have installed on your RPI.
Also be sure that you install at least picamera2 on your host system. This is due to the trick that I am mounting in the docker compose file the libcamera folder of the host into the docker container to make it run.

I hope the issues with using libcamera within a docker container will be resolved soon and i can revert this into something clean.