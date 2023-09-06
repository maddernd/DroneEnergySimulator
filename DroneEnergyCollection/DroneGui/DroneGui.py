import tkinter as tk
import zmq
import json

class DroneGUIClient:
    def __init__(self, master):
        self.master = master
        master.title("Drone Energy Monitor")

        # ZeroMQ setup
        self.context = zmq.Context()
        self.zmq_socket = self.context.socket(zmq.SUB)
        self.zmq_socket.connect("tcp://172.18.0.5:5555")
        self.zmq_socket.setsockopt_string(zmq.SUBSCRIBE, "")

        # UI Setup
        self.label = tk.Label(master, text="Drone Monitor")
        self.label.pack(pady=10)

        # Add an additional label for swarm info
        self.swarm_info_label = tk.Label(master, text="Swarm Info: Average Energy N/A")
        self.swarm_info_label.pack(pady=10)

        # Frame for drone data
        self.drone_frame = tk.Frame(master)
        self.drone_frame.pack(pady=20, padx=20)

        # Drone data dictionary (drone_id -> Label)
        self.drones = {}
        self.energy_data = {}  # for storing drone energy data for average calculation

        # Polling for updates
        self.poll()

    def poll(self):
        try:
            # Check if there's a message without blocking
            raw_data = self.zmq_socket.recv_string(flags=zmq.NOBLOCK)
            drone_data = json.loads(raw_data)

            display_data = f"Drone {drone_data['drone_id']} [State: {drone_data['state']}]: {drone_data['energy']:.2f}% energy remaining"

            if drone_data["drone_id"] in self.drones:
                self.drones[drone_data['drone_id']].config(text=display_data)
            else:
                self.drones[drone_data['drone_id']] = tk.Label(self.drone_frame, text=display_data)
                self.drones[drone_data['drone_id']].pack(anchor='w')
            
            # Update the energy data and average
            self.energy_data[drone_data['drone_id']] = drone_data['energy']
            average_energy = sum(self.energy_data.values()) / len(self.energy_data)
            self.swarm_info_label.config(text=f"Swarm Info: Average Energy {average_energy:.2f}%")
        except zmq.Again:
            pass
        finally:
            # Poll every 1000ms
            self.master.after(1000, self.poll)

if __name__ == "__main__":
    root = tk.Tk()
    app = DroneGUIClient(root)
    root.mainloop()
