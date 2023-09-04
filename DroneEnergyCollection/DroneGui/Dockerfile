FROM python:3.8

WORKDIR /app

# Install system packages for tkinter
RUN apt-get update && apt-get install -y python3-tk && apt-get clean

# Copy the script and the requirements file
COPY . /app

# Install Python packages
RUN pip install pyzmq

CMD ["python", "./DroneGui.py"]
