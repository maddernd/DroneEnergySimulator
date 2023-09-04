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
        self.zmq_socket.connect("tcp://localhost:5555")
        self.zmq_socket.setsockopt_string(zmq.SUBSCRIBE, "")

        # UI Setup
        self.label = tk.Label(master, text="Drone Monitor")
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(master, width=80, height=20)
        self.listbox.pack(pady=20)

        # Drone data dictionary (drone_id -> listbox index)
        self.drones = {}

        # Polling for updates
        self.poll()

    def poll(self):
        try:
            # Check if there's a message without blocking
            raw_data = self.zmq_socket.recv_string(flags=zmq.NOBLOCK)
            drone_data = json.loads(raw_data)
            
            display_data = f"Drone {drone_data['drone_id']} [State: {drone_data['state']}]: {drone_data['energy']:.2f}% energy remaining"

            # If drone is already in the list, update it, otherwise insert new entry
            if drone_data["drone_id"] in self.drones:
                self.listbox.delete(self.drones[drone_data["drone_id"]])
                self.listbox.insert(self.drones[drone_data["drone_id"]], display_data)
            else:
                self.drones[drone_data["drone_id"]] = self.listbox.size()
                self.listbox.insert(tk.END, display_data)
        except zmq.Again:
            pass
        finally:
            # Poll every 1000ms
            self.master.after(1000, self.poll)

if __name__ == "__main__":
    root = tk.Tk()
    app = DroneGUIClient(root)
    root.mainloop()
