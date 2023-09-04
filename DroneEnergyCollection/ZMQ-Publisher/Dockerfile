FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install zmq paho-mqtt

CMD ["python", "./ZMQ-Publisher.py"]
