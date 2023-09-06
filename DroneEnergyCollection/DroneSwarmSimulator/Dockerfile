# Use an official Python runtime as the parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install necessary packages
RUN pip3 install zmq paho-mqtt

# Default environment variables (can be overridden by Kubernetes at runtime)
ENV SWARM_NAME=DefaultSwarm

# Run DroneSwarm1.py when the container launches
CMD ["python", "./DroneSwarm1.py"]
