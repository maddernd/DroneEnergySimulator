import zmq

def forwarder(input_address, output_address):
    context = zmq.Context()
    
    # Socket to receive messages
    frontend = context.socket(zmq.PULL)
    frontend.bind(input_address)
    
    # Socket to send messages
    backend = context.socket(zmq.PUB)
    backend.bind(output_address)
    
    zmq.device(zmq.FORWARDER, frontend, backend)

if __name__ == "__main__":
    forwarder("tcp://*:6000", "tcp://*:6001")
