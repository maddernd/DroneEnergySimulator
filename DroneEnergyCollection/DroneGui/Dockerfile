# Use an official Python runtime as the parent image
FROM python:3.8-slim

# Install the required system packages
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install necessary packages
RUN pip3 install zmq paho-mqtt

# Run DroneGui.py when the container launches
CMD ["python", "./DroneGui.py"]

# X11 forwarding for GUI
ENV DISPLAY=unix$DISPLAY

# Run as root (for now; this can be tightened up)
USER root
