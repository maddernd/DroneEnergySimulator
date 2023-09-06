import random
import logging
import zmq
import time
import json
import os
from Drone import Drone 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
def simulate_drones(num_drones, publisher_address, swarm_name):

    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.connect(publisher_address)
    
    drones = [Drone(i, max_energy=random.uniform(80, 120)) for i in range(num_drones)]
    
    while True:
        for drone in drones:
            drone.consume_energy()
            drone.change_state()
            drone_data = {
                "drone_id": drone.drone_id,
                "state": drone.current_state,
                "energy": drone.energy,
                "swarm": swarm_name
            }
            socket.send_string(json.dumps(drone_data))
            time.sleep(1)

if __name__ == "__main__":
        swarm_name = os.environ.get("SWARM_NAME", "DefaultSwarm")
        simulate_drones(20, "tcp://publisher-service:6000", swarm_name)
