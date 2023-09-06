# Use an official Python runtime as the parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install necessary packages
RUN pip3 install zmq paho-mqtt

# Run Publisher-Service.py when the container launches
CMD ["python", "./Publisher-Service.py"]
