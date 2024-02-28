#!/bin/bash

# Define the target device (the same as in your start script)
DEVICE="/dev/video0"

# Find the ffmpeg process streaming to the virtual camera and kill it
PID=$(pgrep -f "ffmpeg.*$DEVICE")

if [ ! -z "$PID" ]; then
    echo "Stopping ffmpeg process streaming to $DEVICE..."
    kill $PID
    echo "ffmpeg process stopped."
else
    echo "No ffmpeg process found streaming to $DEVICE."
fi

# Optional: Unload the v4l2loopback module if not needed anymore
# sudo modprobe -r v4l2loopback
# echo "v4l2loopback module unloaded."
