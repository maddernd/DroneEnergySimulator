import zmq
import paho.mqtt.client as mqtt

BROKER = "localhost"  # Your MQTT broker's address
PORT = 1883
MQTT_TOPIC = "drones/data"

# ZeroMQ Subscriber Setup
context = zmq.Context()
zmq_socket = context.socket(zmq.SUB)
zmq_socket.connect("tcp://localhost:5555")
zmq_socket.setsockopt_string(zmq.SUBSCRIBE, "")

# MQTT Client Setup
mqtt_client = mqtt.Client("DronePublisher")
mqtt_client.connect(BROKER, PORT)

while True:
    drone_data = zmq_socket.recv_string()
    mqtt_client.publish(MQTT_TOPIC, drone_data)
