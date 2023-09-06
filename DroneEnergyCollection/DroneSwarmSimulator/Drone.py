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
