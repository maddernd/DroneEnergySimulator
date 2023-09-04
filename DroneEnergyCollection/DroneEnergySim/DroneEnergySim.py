import random
import logging
import zmq
import time
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Drone:
    def __init__(self, drone_id, max_energy=100):
        self.drone_id = drone_id
        self.max_energy = max_energy
        self.energy = self.max_energy
        self.states = ["idle", "hovering", "moving"]
        self.current_state = random.choice(self.states)

        # Random factors for simulating real-world events
        self.wind_resistance = random.uniform(0.8, 1.2)
        self.drone_efficiency = random.uniform(0.9, 1.1)

    def consume_energy(self):
        consumption_rate = {
            "idle": 0.2,
            "hovering": 1.5,
            "moving": 2.5
        }

        # Factor in the wind resistance and drone efficiency
        self.energy -= consumption_rate[self.current_state] * self.wind_resistance * self.drone_efficiency

        # Energy can't go below 0
        self.energy = max(0, self.energy)

        # If energy is too low, simulate a return to home and recharge
        if self.energy < 10:
            self.return_to_home_and_recharge()
            logging.warning(f"Drone {self.drone_id} energy is critically low!")

    def change_state(self):
        if random.uniform(0, 1) < 0.1:
            self.current_state = random.choice(self.states)
            logging.info(f"Drone {self.drone_id} changed state to {self.current_state}")

    def return_to_home_and_recharge(self):
        logging.info(f"Drone {self.drone_id} returning to home for recharge!")
        self.energy = self.max_energy
        self.current_state = "idle"

    def __str__(self):
        return f"Drone {self.drone_id} [State: {self.current_state}]: {self.energy:.2f}% energy remaining"

class DronePublisher:
    def __init__(self, port="5555"):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{port}")

    def send_data(self, drone):
        drone_data = {
            "drone_id": drone.drone_id,
            "state": drone.current_state,
            "energy": drone.energy
        }
        self.socket.send_string(json.dumps(drone_data))

def simulate_drones(num_drones, duration, publisher=None):
    drones = [Drone(i, max_energy=random.uniform(80, 120)) for i in range(num_drones)]
    end_time = time.time() + duration

    while time.time() < end_time:
        for drone in drones:
            drone.consume_energy()
            drone.change_state()

            # Convert the drone object to a string for printing
            drone_data = str(drone)
            print(drone_data)
            
            # If a publisher is available, send the drone object for publishing
            if publisher:
                publisher.send_data(drone)
            
            time.sleep(1)


# For testing
if __name__ == "__main__":
    drone = Drone(1)
    for _ in range(10):
        drone.consume_energy()
        drone.change_state()
        print(drone)
    
    # Simulating multiple drones
    NUM_DRONES = 5
    DURATION = 120
    publisher = DronePublisher()
    simulate_drones(NUM_DRONES, DURATION, publisher)